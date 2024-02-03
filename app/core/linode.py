from linode_api4 import LinodeClient, Instance

from app.core.config import config


def get_client():
    return LinodeClient(config.LINODE_TOKEN)


client = get_client()
