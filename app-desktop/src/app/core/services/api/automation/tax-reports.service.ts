import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import type { LivrosFiscaisRequest } from '../../../models/automation/livros-fiscais-request.model';
import type { Observable } from 'rxjs';
import { BackendService } from '../backend.service';
import type { CancelledInvoicesRequest } from '../../../models/automation/cancelled-invoices-request.model';

@Injectable({ providedIn: 'root' })
export class TaxReportsService {
  private readonly http: HttpClient = inject(HttpClient);
  private readonly backend = inject(BackendService);

  execute(request: LivrosFiscaisRequest): Observable<void> {
    return this.http.post<void>(`${this.backend.api}/automation/tax-reports/run`, request);
  }

  generateCancelledInvoicesReport(request: CancelledInvoicesRequest): Observable<void> {
    return this.http.post<void>(`${this.backend.api}/automation/cancelled-invoices/run`, request);
  }
}
