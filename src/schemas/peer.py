from typing import Optional
from pydantic import BaseModel


class PeerCompany(BaseModel):

    company_id: str

    company_name: str

    company_logo: Optional[str] = None

    peer_group_name: str

    is_benchmark: bool

    class Config:
        from_attributes = True