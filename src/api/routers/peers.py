from fastapi import APIRouter

router = APIRouter()

from typing import List

from fastapi import APIRouter

from src.schemas.peer import PeerCompany
from src.services.peer_service import get_peer_group

router = APIRouter()


@router.get(
    "/peers/{group_name}",
    response_model=List[PeerCompany]
)
def peer_group(group_name: str):

    return get_peer_group(group_name)