from pydantic import BaseModel

from shared.application.dto.branch_group.branch_group_response_dto import BranchGroupResponseDTO


class BranchGroupWithBranchesDTO(BaseModel):
    id: int
    name: str
    analyst: str
    branches: list[BranchGroupResponseDTO]
