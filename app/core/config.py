import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    LINODE_TOKEN: str = os.getenv("LINODE_TOKEN")
    SSH_PASSWD: str = os.getenv("SSH_PASSWD")
    CF_TOKEN: str = os.getenv("CF_TOKEN")
    CF_DOMAIN: str = os.getenv("CF_DOMAIN")
    CF_ZONEID: str = os.getenv("CF_ZONEID")


config = Config()
