from pydantic import BaseModel

from shared.domain.entities.branch_group import BranchGroup


class BranchGroupResponseDTO(BaseModel):
    id: int | None
    codigo: str
    name: str

    @classmethod
    def from_entity(cls, group: BranchGroup):
        return cls(id=group.id, codigo=group.codigo, name=group.name)
