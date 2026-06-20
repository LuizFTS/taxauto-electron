import datetime
import os

import pandas as pd

from modules.data_process.audits.cancelled_invoices.constants.discrepancy_catalog import (
    RULE1,
    RULE2,
    resolve_rule3_entry,
)
from modules.data_process.audits.cancelled_invoices.services.load_and_merge_date_service import (
    LoadAndMergeDataService,
)
from modules.data_process.domain.entities.AuditDiscrepancy import AuditSummary


class AuditCancelledInvoicesUseCase:
    def __init__(self, load_and_merge_data_service: LoadAndMergeDataService):
        self.load_and_merge_data_service = load_and_merge_data_service

    def execute(self, book_path: str, portal_path: str) -> AuditSummary:
        processed_data = self.load_and_merge_data_service.execute(book_path, portal_path)
        df = processed_data["merged_data"]

        # ── Máscaras ─────────────────────────────────────────────────────────────
        is_canceled_in_book = (
            df["Observação"].str.upper().fillna("").str.contains("INUTILIZADA|NF CANCELADA")
        )
        rule1_mask = is_canceled_in_book & (df["_merge"] == "left_only")
        rule2_mask = ~is_canceled_in_book & (df["_merge"] == "both")
        rule3_mask = df["_merge"] == "right_only"

        # ── Coluna de resultado ───────────────────────────────────────────────────
        df["Resultado Auditoria"] = "OK"
        df.loc[rule1_mask, "Resultado Auditoria"] = RULE1.audit_label
        df.loc[rule2_mask, "Resultado Auditoria"] = RULE2.audit_label

        if rule3_mask.any():
            df.loc[rule3_mask, "Resultado Auditoria"] = (
                df.loc[rule3_mask, "portal_Status Doc"]
                .fillna("Desconhecido")
                .apply(lambda s: resolve_rule3_entry(s).audit_label)
            )

        # ── Exportação ────────────────────────────────────────────────────────────
        cols_to_export = [c for c in df.columns if c not in ("_merge", "composite_key")]
        df_all = df[cols_to_export].copy()
        df_errors = df.loc[df["Resultado Auditoria"] != "OK", cols_to_export].copy()

        export_path = self._export(df_all, df_errors)

        # ── Discrepâncias ─────────────────────────────────────────────────────────
        discrepancies = []

        for mask, entry in ((rule1_mask, RULE1), (rule2_mask, RULE2)):
            subset = df[mask]
            if not subset.empty:
                discrepancies.append(entry.to_audit_discrepancy(len(subset)))

        # Regra 3: agrupa por status para gerar uma discrepância por tipo
        if rule3_mask.any():
            rule3_df = df[rule3_mask]
            for status, group in rule3_df.groupby("portal_Status Doc"):
                entry = resolve_rule3_entry(str(status))
                discrepancies.append(entry.to_audit_discrepancy(len(group)))

        # ── Métricas ──────────────────────────────────────────────────────────────
        total_audited = processed_data["book_count"]
        total_errors = sum(d.count for d in discrepancies)
        compliance_rate = (
            round(((total_audited - total_errors) / total_audited) * 100, 2)
            if total_audited > 0
            else 100.0
        )

        return AuditSummary(
            total_audited=total_audited,
            compliance_rate=compliance_rate,
            discrepancies=discrepancies,
            report_path=export_path,
        )

    def _export(self, df_all: pd.DataFrame, df_errors: pd.DataFrame) -> str:
        app_data_path = os.getenv("LOCALAPPDATA")

        if app_data_path is None:
            raise Exception("Nenhum diretório de armazenamento encontrado.")

        export_dir = os.path.join(app_data_path, "TaxAuto", "AuditReports")
        os.makedirs(export_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        export_path = os.path.join(export_dir, f"relatorio_auditoria_{timestamp}.xlsx")

        try:
            with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
                df_errors.to_excel(writer, sheet_name="Divergências", index=False)
                df_all.to_excel(writer, sheet_name="Auditoria Completa", index=False)
            print(f"Relatório exportado em: {export_path}")
        except Exception as e:
            print(f"Falha ao exportar relatório: {e}")
            export_path = ""

        return export_path
