from dataclasses import dataclass
from typing import List


@dataclass
class AuditDiscrepancy:
    title: str
    count: int
    severity: str  # "CRITICAL", "WARNING"
    description: str


@dataclass
class AuditSummary:
    total_audited: int
    compliance_rate: float
    discrepancies: List[AuditDiscrepancy]
    report_path: str
