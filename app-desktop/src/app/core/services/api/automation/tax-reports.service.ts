import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import type { LivrosFiscaisRequest } from '../../../models/automation/livros-fiscais-request.model';
import type { Observable } from 'rxjs';
import { BackendService } from '../backend.service';
import type {
  CancelledInvoicesFlowRequest,
  CancelledInvoicesRequest,
} from '../../../models/automation/cancelled-invoices-request.model';
import type { AuditCancelledInvoicesResponse } from '../../../models/api/response/cancelled-invoices/audit-cancelled-invoices.model';
import type { TaxAssessmentReportRequest } from '../../../models/automation/tax-assessment-report-request.model';

@Injectable({ providedIn: 'root' })
export class TaxReportsService {
  private readonly http: HttpClient = inject(HttpClient);
  private readonly backend = inject(BackendService);

  execute(request: LivrosFiscaisRequest): Observable<void> {
    return this.http.post<void>(`${this.backend.api}/automation/tax-books/run`, request);
  }

  generateTaxAssessmentReports(request: TaxAssessmentReportRequest): Observable<void> {
    return this.http.post<void>(`${this.backend.api}/automation/tax-reports/assessment`, request);
  }

  generateCancelledInvoicesReport(request: CancelledInvoicesRequest): Observable<void> {
    return this.http.post<void>(`${this.backend.api}/automation/cancelled-invoices/run`, request);
  }

  generateCancelledInvoicesReportFlow(
    request: CancelledInvoicesFlowRequest,
  ): Observable<AuditCancelledInvoicesResponse> {
    return this.http.post<AuditCancelledInvoicesResponse>(
      `${this.backend.api}/automation/cancelled-invoices-flow/run`,
      request,
    );
  }

  validateCancelledInvoiceFile(payload: {
    file_path: string;
    file_type: string;
  }): Observable<{ is_valid: boolean; record_count: number; message: string }> {
    return this.http.post<{ is_valid: boolean; record_count: number; message: string }>(
      `${this.backend.api}/automation/cancelled-invoices/validate-file`,
      payload,
    );
  }
}
