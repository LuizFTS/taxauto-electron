from typing import Optional

from pydantic import BaseModel


class NotaFiscalBase(BaseModel):
    branch: str
    number_tax_invoice: str

    @property
    def key(self) -> str:
        return f"{str(self.branch).zfill(3)}_{str(self.number_tax_invoice).zfill(9)}"


class NotaLivro(NotaFiscalBase):
    status_livro: str
    valor: Optional[float] = None


class NotaPortal(NotaFiscalBase):
    status_portal: str = "CANCELADA"
