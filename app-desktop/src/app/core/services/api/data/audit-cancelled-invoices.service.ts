import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { BackendService } from '../backend.service';
import type { Observable } from 'rxjs';
import type { AuditCancelledInvoicesResponse } from '../../../models/api/response/cancelled-invoices/audit-cancelled-invoices.model';
import type { AuditCancelledInvoicesReportEntry } from '../../../models/api/response/cancelled-invoices/audit-cancelled-invoices-report-entry.model';

@Injectable({
  providedIn: 'root',
})
export class AuditCancelledInvoicesService {
  private readonly http: HttpClient = inject(HttpClient);
  private readonly backend = inject(BackendService);

  public run(bookPath: string, portalPath: string): Observable<AuditCancelledInvoicesResponse> {
    return this.http.post<AuditCancelledInvoicesResponse>(
      `${this.backend.api}/taxdata/cancelled-invoices/run`,
      {
        book_path: bookPath,
        portal_path: portalPath,
      },
    );
  }

  public getAuditByFileName(fileName: string): Observable<AuditCancelledInvoicesResponse> {
    return this.http.get<AuditCancelledInvoicesResponse>(
      `${this.backend.api}/taxdata/cancelled-invoices/report?report_name=${fileName}`,
    );
  }

  public getAllAudits(): Observable<AuditCancelledInvoicesReportEntry[]> {
    return this.http.get<AuditCancelledInvoicesReportEntry[]>(
      `${this.backend.api}/taxdata/cancelled-invoices/reports`,
    );
  }

  public deleteAuditByFileName(fileName: string): Observable<void> {
    return this.http.delete<void>(
      `${this.backend.api}/taxdata/cancelled-invoices/report?report_name=${fileName}`,
    );
  }
}
