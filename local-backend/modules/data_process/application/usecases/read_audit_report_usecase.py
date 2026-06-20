import os
from typing import List

import pandas as pd

from modules.data_process.audits.cancelled_invoices.constants.discrepancy_catalog import (
    RULE1,
    RULE2,
    RULE3_CATALOG,
)
from modules.data_process.domain.entities.AuditDiscrepancy import (
    AuditDiscrepancy,
    AuditSummary,
)


class ReadAuditReportUseCase:
    AUDIT_RESULT_COLUMN = "Resultado Auditoria"
    OK_VALUE = "OK"

    def execute(self, report_name: str) -> AuditSummary:

        app_data_path = os.getenv("LOCALAPPDATA")

        if app_data_path is None:
            raise Exception("Nenhum diretório de armazenamento encontrado.")

        export_dir = os.path.join(app_data_path, "TaxAuto", "AuditReports")
        report_path = os.path.join(export_dir, report_name)

        if not os.path.exists(report_path):
            raise FileNotFoundError(f"Relatório não encontrado: {report_path}")

        # ── Lê a aba completa (fonte da verdade) ─────────────────────────────
        try:
            df = pd.read_excel(report_path, sheet_name="Auditoria Completa", dtype=str)
        except Exception as e:
            raise ValueError(f"Falha ao ler o relatório '{report_path}': {e}")

        if self.AUDIT_RESULT_COLUMN not in df.columns:
            raise ValueError(
                f"Coluna '{self.AUDIT_RESULT_COLUMN}' não encontrada. "
                "Verifique se o arquivo foi gerado por esta aplicação."
            )

        df[self.AUDIT_RESULT_COLUMN] = (
            df[self.AUDIT_RESULT_COLUMN].fillna(self.OK_VALUE).str.strip()
        )

        # ── Métricas ──────────────────────────────────────────────────────────
        total_audited = len(df)
        df_errors = df[df[self.AUDIT_RESULT_COLUMN] != self.OK_VALUE]
        total_errors = len(df_errors)

        compliance_rate = 100.0
        if total_audited > 0:
            compliance_rate = round(((total_audited - total_errors) / total_audited) * 100, 2)

        # --- Mapeamento para Reconstrução ---
        # Criamos um mapa de 'audit_label' -> 'DiscrepancyEntry' para facilitar a busca
        lookup_map = {entry.audit_label: entry for entry in [RULE1, RULE2]}

        # Adiciona as variações da Regra 3 ao mapa de busca
        for entry in RULE3_CATALOG.values():
            lookup_map[entry.audit_label] = entry

        discrepancies: List[AuditDiscrepancy] = []
        error_counts = df_errors.groupby(self.AUDIT_RESULT_COLUMN).size()

        for error_label, count in error_counts.items():
            entry = lookup_map.get(error_label)

            if entry:
                # Usa o método auxiliar da dataclass para converter
                discrepancies.append(entry.to_audit_discrepancy(count=int(count)))
            else:
                # Fallback para erros desconhecidos ou gerados dinamicamente pela Rule 3
                discrepancies.append(
                    AuditDiscrepancy(
                        title=f"Divergência: {error_label}",
                        count=int(count),
                        severity="ERRO",
                        description="Tipo de divergência não catalogado ou dinâmico.",
                    )
                )

        return AuditSummary(
            total_audited=total_audited,
            compliance_rate=compliance_rate,
            discrepancies=discrepancies,
            report_path=report_path,
        )
