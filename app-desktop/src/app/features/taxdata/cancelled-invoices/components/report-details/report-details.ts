import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { LoadingService, AuditCancelledInvoicesService } from '../../../../../core';
import type { AuditCancelledInvoicesResponse } from '../../../../../core/models/api/response/cancelled-invoices/audit-cancelled-invoices.model';

@Component({
  selector: 'app-report-details',
  imports: [CommonModule],
  templateUrl: './report-details.html',
  styleUrl: './report-details.scss',
})
export class ReportDetails implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly auditService = inject(AuditCancelledInvoicesService);
  private readonly router = inject(Router);
  private loadingService = inject(LoadingService);

  audit: AuditCancelledInvoicesResponse | null = null;
  readonly fileName = this.route.snapshot.paramMap.get('fileName');

  ngOnInit(): void {
    if (this.fileName) {
      this.loadAudit(this.fileName);
    }
  }

  private loadAudit(fileName: string): void {
    this.loadingService.show();
    this.auditService.getAuditByFileName(fileName).subscribe({
      next: (audit) => {
        this.audit = audit;
        console.log(audit);
        this.loadingService.hide();
      },
      error: (error) => {
        console.error('Error loading audit:', error);
        this.loadingService.hide();
      },
    });
  }

  voltar(): void {
    this.router.navigate(['/taxdata/cancelled-invoices']);
  }

  verRelatorioCompleto(reportPath: string): void {
    if (!reportPath) {
      return;
    }
    window.electron.openExternal(reportPath);
  }

  complianceWidth(value: number): number {
    if (Number.isNaN(value)) {
      return 0;
    }
    return Math.max(0, Math.min(100, value));
  }

  metricPercent(count: number): number {
    const total = this.audit?.discrepancies?.reduce((sum, item) => sum + item.count, 0) ?? 0;
    if (!total) {
      return 0;
    }
    return Math.max(4, (count / total) * 100);
  }

  severityClass(severity: string): string {
    switch (severity) {
      case 'CRITICO':
        return 'report-item__chip--critical';
      case 'ALTO':
        return 'report-item__chip--high';
      case 'MEDIO':
        return 'report-item__chip--medium';
      case 'BAIXO':
        return 'report-item__chip--low';
      default:
        return '';
    }
  }

  // function to sum all values of count of each discrepancy
  get sumAllCounts(): number {
    return this.audit?.discrepancies?.reduce((sum, item) => sum + item.count, 0) ?? 0;
  }
}
