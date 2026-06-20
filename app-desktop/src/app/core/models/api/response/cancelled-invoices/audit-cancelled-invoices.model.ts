export interface AuditCancelledInvoicesResponse {
  total_audited: number;
  compliance_rate: number;
  discrepancies: AuditDiscrepancy[];
  report_path: string;
}

export interface AuditDiscrepancy {
  title: string;
  count: number;
  severity: string;
}
