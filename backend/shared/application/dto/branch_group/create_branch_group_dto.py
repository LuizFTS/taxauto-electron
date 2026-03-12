from pydantic import BaseModel


class CreateBranchGroupDTO(BaseModel):
    code: str
    name: str
    analyst: str
