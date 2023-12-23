from typing import Union, Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status

from linode_api4 import LinodeClient, Instance
from dotenv import load_dotenv
import os
import paramiko

app = FastAPI()
paramiko.util.log_to_file("paramiko.log")
load_dotenv()
LINODE_TOKEN = os.getenv("LINODE_TOKEN")
SSH_KEY = os.getenv("SSH_KEY")
SSH_PASSWD = os.getenv("SSH_PASSWD")
# Create a single Linode API client
linode_client = LinodeClient(LINODE_TOKEN)

templates = Jinja2Templates(directory="app")

region_list = ["jp-osa", "ap-south", "eu-central", "us-east"]
expiration_list = ["1 hour", "2 hours", "3 hours", "6 hours", "12 hours", "never"]

# references for created instances
instance_dict = {}


@app.get("/", response_class=HTMLResponse)
def get_status(request: Request):
    # List all Linodes on the account
    linode_list = linode_client.linode.instances()
    # Update local instance dict on first start
    if len(instance_dict) == 0 and len(linode_list) > 0:
        for item in linode_list:
            instance_dict[item.label] = item
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "region_list": linode_client.regions(),
            "expiration_list": expiration_list,
            "linode_list": linode_list,
        },
    )


@app.post("/")
async def create_instance(
    region: Annotated[str, Form()], expiration: Annotated[str, Form()]
):
    # Create a new Linode
    new_linode = linode_client.linode.instance_create(
        ltype="g6-nanode-1",
        region=region,
        image="linode/debian12",
        label="wg0-" + region,
        authorized_keys=[SSH_KEY],
        root_pass=SSH_PASSWD,
    )
    print(
        "{instance_id} ({instance_ipv4}) created".format(
            instance_id=new_linode.label, instance_ipv4=new_linode.ipv4[0]
        )
    )
    return RedirectResponse(
        "/", status_code=status.HTTP_302_FOUND
    )  # without status_code original method is carried over but undesirable in this case


@app.get("/{instance_id}")
async def delete_instance(instance_id: str):
    instance = instance_dict[instance_id]
    print(
        "{instance_id} ({instance_ipv4}) deleted".format(
            instance_id=instance_id, instance_ipv4=instance.ipv4[0]
        )
    )
    instance.delete()
    return RedirectResponse("/")


@app.get("/{instance_id}/up")
async def setup_wireguard(instance_id: str):
    instance_ipv4 = instance_dict[instance_id].ipv4[0]
    # install wireguard
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.WarningPolicy())
    sshClient.connect(instance_ipv4, username="root", password=SSH_PASSWD)
    stdin, stdout, stderr = sshClient.exec_command(
        "apt update && apt install -y wireguard iptables"
    )
    exit_status = stdout.channel.recv_exit_status()
    stdin, stdout, stderr = sshClient.exec_command("sysctl -w net.ipv4.ip_forward=1")
    exit_status = stdout.channel.recv_exit_status()
    # add wireguard config
    sftpClient = sshClient.open_sftp()
    filepath = "/etc/wireguard/wg0.conf"
    localpath = "app/wg/wg0.conf"
    sftpClient.put(localpath, filepath)
    # up wireguard
    stdin, stdout, stderr = sshClient.exec_command("wg-quick up wg0")
    exit_status = stdout.channel.recv_exit_status()
    sftpClient.close()
    sshClient.close()
    print(
        "{instance_id} ({instance_ipv4}) set".format(
            instance_id=instance_id, instance_ipv4=instance_ipv4
        )
    )
    return RedirectResponse("/")
