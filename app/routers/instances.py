from typing import Annotated
from fastapi import Request, Form
import starlette.status as status
from fastapi import APIRouter, HTTPException

from app.core import linode, wireguard, cloudflare
from app.core.config import config

router = APIRouter()


@router.get("/", tags=["instances"])
def get_instances(request: Request):
    # List all Linodes on the account
    linode_list = linode.client.linode.instances()
    return linode_list


@router.post("/", tags=["instances"])
def create_instance(region: Annotated[str, Form()], expiration: Annotated[int, Form()]):
    new_linode = linode.create_instance(region, expiration)
    if not new_linode:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create instance with region={region}, expiration={expiration}",
        )
    return {"status": "ok"}


@router.delete("/{instance_label}/kill", tags=["instances"])
def delete_instance(instance_label: str):
    success = linode.delete_instance(instance_label)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete {instance_label}",
        )
    return {"status": "ok"}


@router.put("/{instance_label}/up", tags=["instances"])
def setup_wireguard(instance_label: str):
    success = wireguard.setup(instance_label)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to setup wireguard {instance_label}",
        )
    return {"status": "ok"}


@router.put("/{instance_label}/dns", tags=["instances"])
def setup_dns(instance_label: str):
    success = cloudflare.update_dns(instance_label)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update cloudflare dns {instance_label}",
        )
    return {"status": "ok"}
