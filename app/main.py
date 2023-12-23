from typing import Union, Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status

from linode_api4 import LinodeClient, Instance
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()
LINODE_TOKEN = os.getenv("LINODE_TOKEN")
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
            "region_list": region_list,
            "expiration_list": expiration_list,
            "linode_list": linode_list,
        },
    )


@app.post("/")
async def create_instance(
    region: Annotated[str, Form()], expiration: Annotated[str, Form()]
):
    # Create a new Linode
    new_linode, root_pass = linode_client.linode.instance_create(
        ltype="g6-nanode-1",
        region=region,
        image="linode/debian12",
        label="wg0-" + region,
    )

    print(new_linode.label, " created")
    return RedirectResponse(
        "/", status_code=status.HTTP_302_FOUND
    )  # without status_code original method is carried over but undesirable in this case


@app.get("/{instance_id}")
async def delete_instance(instance_id: str):
    instance_dict[instance_id].delete()
    print(instance_id, " deleted")
    return RedirectResponse("/")
