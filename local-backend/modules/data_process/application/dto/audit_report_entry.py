from dataclasses import dataclass


@dataclass
class AuditReportEntry:
    file_name: str
    report_path: str
    generated_at: str
