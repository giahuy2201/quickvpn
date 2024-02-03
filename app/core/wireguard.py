import paramiko

from app.core.config import config
from app.core.linode import get_instance


def setup(instance_label: str):
    # retrieve instance
    instance = get_instance(instance_label)
    instance_ipv4 = instance.ipv4[0]
    # install wireguard
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.WarningPolicy())
    sshClient.connect(instance_ipv4, username="root", password=config.SSH_PASSWD)
    stdin, stdout, stderr = sshClient.exec_command(
        "apt update && apt install -y wireguard iptables"
    )
    exit_status = stdout.channel.recv_exit_status()
    stdin, stdout, stderr = sshClient.exec_command("sysctl -w net.ipv4.ip_forward=1")
    exit_status = stdout.channel.recv_exit_status()
    # add wireguard config
    sftpClient = sshClient.open_sftp()
    filepath = "/etc/wireguard/wg0.conf"
    localpath = "config/wg0.conf"
    sftpClient.put(localpath, filepath)
    # up wireguard
    stdin, stdout, stderr = sshClient.exec_command("wg-quick up wg0")
    exit_status = stdout.channel.recv_exit_status()
    sftpClient.close()
    sshClient.close()
    if exit_status == 0:
        print(f"{instance_label} ({instance_ipv4}) wireguard set")
        return True
    return False
