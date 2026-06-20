import os


class DeleteAuditReportUseCase:
    def execute(self, report_name: str):
        app_data_path = os.getenv("LOCALAPPDATA")

        if app_data_path is None:
            raise Exception("Nenhum diretório de armazenamento encontrado.")
        export_dir = os.path.join(app_data_path, "TaxAuto", "AuditReports")
        report_path = os.path.join(export_dir, report_name)

        if not os.path.exists(report_path):
            raise FileNotFoundError(f"Relatório não encontrado: {report_path}")

        try:
            os.remove(report_path)
        except Exception as e:
            raise ValueError(f"Falha ao deletar o relatório '{report_path}': {e}")
