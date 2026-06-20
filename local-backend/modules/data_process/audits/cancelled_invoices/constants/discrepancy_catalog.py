from dataclasses import dataclass

from modules.data_process.domain.entities.AuditDiscrepancy import AuditDiscrepancy


@dataclass(frozen=True)
class DiscrepancyEntry:
    audit_label: str  # valor que vai na coluna "Resultado Auditoria"
    title: str
    severity: str
    description: str

    def to_audit_discrepancy(self, count: int) -> AuditDiscrepancy:
        return AuditDiscrepancy(
            title=self.title,
            count=count,
            severity=self.severity,
            description=self.description,
        )


# Entradas fixas (regras 1 e 2)
RULE1 = DiscrepancyEntry(
    audit_label="Erro: Cancelada no Livro, mas Ativa no PortalGED",
    title="Divergência: Cancelamento não confirmado no PortalGED",
    severity="CRÍTICO",
    description=(
        "Notas marcadas como canceladas no Livro Fiscal que constam " "como ATIVAS na SEFAZ."
    ),
)

RULE2 = DiscrepancyEntry(
    audit_label="Erro: Ativa no Livro, mas Cancelada no PortalGED",
    title="Divergência: Nota Cancelada no PortalGED consta como Ativa",
    severity="CRÍTICO",
    description=(
        "Notas canceladas no PortalGED que não tiveram baixa no Livro Fiscal. "
        "Risco fiscal: imposto sendo apurado sobre nota inexistente."
    ),
)

# Entradas dinâmicas (regra 3 — dependem do status do portal)
RULE3_CATALOG: dict[str, DiscrepancyEntry] = {
    "CANCELADA": DiscrepancyEntry(
        audit_label="Erro: Cancelada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Cancelada no Portal, ausente no Livro",
        severity="CRÍTICO",
        description="Notas canceladas na SEFAZ sem registro no Livro Fiscal.",
    ),
    "CANCELADO": DiscrepancyEntry(
        audit_label="Erro: Cancelada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Cancelada no Portal, ausente no Livro",
        severity="CRÍTICO",
        description="Notas canceladas na SEFAZ sem registro no Livro Fiscal.",
    ),
    "INUTILIZADA": DiscrepancyEntry(
        audit_label="Erro: Inutilizada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Inutilizada no Portal, ausente no Livro",
        severity="CRÍTICO",
        description="Notas inutilizadas na SEFAZ sem registro no Livro Fiscal.",
    ),
    "INUTILIZADO": DiscrepancyEntry(
        audit_label="Erro: Inutilizada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Inutilizada no Portal, ausente no Livro",
        severity="CRÍTICO",
        description="Notas inutilizadas na SEFAZ sem registro no Livro Fiscal.",
    ),
    "REJEITADA": DiscrepancyEntry(
        audit_label="Erro: Rejeitada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Rejeitada no Portal, ausente no Livro",
        severity="ALERTA",
        description="Notas rejeitadas pela SEFAZ sem correspondência no Livro Fiscal.",
    ),
    "REJEITADO": DiscrepancyEntry(
        audit_label="Erro: Rejeitada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Rejeitada no Portal, ausente no Livro",
        severity="ALERTA",
        description="Notas rejeitadas pela SEFAZ sem correspondência no Livro Fiscal.",
    ),
    "DENEGADA": DiscrepancyEntry(
        audit_label="Erro: Denegada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Denegada no Portal, ausente no Livro",
        severity="ALERTA",
        description="Notas denegadas pela SEFAZ sem correspondência no Livro Fiscal.",
    ),
    "DENEGADO": DiscrepancyEntry(
        audit_label="Erro: Denegada no Portal, mas ausente no Livro Fiscal",
        title="Divergência: Denegada no Portal, ausente no Livro",
        severity="ALERTA",
        description="Notas denegadas pela SEFAZ sem correspondência no Livro Fiscal.",
    ),
}


def resolve_rule3_entry(status_raw: str) -> DiscrepancyEntry:
    """Retorna a entrada do catálogo para um status do portal, com fallback."""
    normalized = str(status_raw).strip().upper()
    return RULE3_CATALOG.get(
        normalized,
        DiscrepancyEntry(
            audit_label=f"Erro: Nota ausente no Livro Fiscal (Status Portal: {status_raw})",
            title="Divergência: Nota ausente no Livro Fiscal",
            severity="CRÍTICO",
            description=f"Nota com status '{status_raw}' no portal sem registro no Livro Fiscal.",
        ),
    )
