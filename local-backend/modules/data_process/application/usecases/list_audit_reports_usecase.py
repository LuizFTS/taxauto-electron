import glob
import os
from datetime import datetime
from typing import List

from modules.data_process.application.dto.audit_report_entry import AuditReportEntry


class ListAuditReportsUseCase:
    def execute(self) -> List[AuditReportEntry]:
        app_data_path = os.getenv("LOCALAPPDATA")

        if app_data_path is None:
            raise Exception("Nenhum diretório de armazenamento encontrado.")
        export_dir = os.path.join(app_data_path, "TaxAuto", "AuditReports")

        if not os.path.exists(export_dir):
            return []

        files = sorted(
            glob.glob(os.path.join(export_dir, "relatorio_auditoria_*.xlsx")),
            reverse=True,  # mais recente primeiro
        )

        entries = []
        for path in files:
            name = os.path.basename(path)
            # extrai "20250610_143022" do nome do arquivo
            timestamp_str = name.removeprefix("relatorio_auditoria_").removesuffix(".xlsx")
            try:
                dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                generated_at = dt.strftime("%d/%m/%Y %H:%M:%S")
            except ValueError:
                generated_at = "Data desconhecida"

            print(name)
            print(generated_at)

            entries.append(
                AuditReportEntry(
                    file_name=name,
                    report_path=path,
                    generated_at=generated_at,
                )
            )

        return entries
