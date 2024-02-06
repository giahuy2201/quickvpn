from app.core import linode


from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{provider_name}/regions", tags=["providers"])
def get_regions(provider_name: str):
    return linode.get_all_regions()
