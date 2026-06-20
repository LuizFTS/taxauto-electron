import {
  ChangeDetectorRef,
  Component,
  ChangeDetectionStrategy,
  inject,
  signal,
  OnInit,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { Button } from '../../../shared';
import { MatIconModule } from '@angular/material/icon';
import { DragAndDropArea } from './components/drag-and-drop-area/drag-and-drop-area';
import { LoadingService } from '../../../core/services/loading.service';
import { AuditCancelledInvoicesService } from '../../../core/services/api/data/audit-cancelled-invoices.service';
import type { AuditCancelledInvoicesReportEntry } from '../../../core/models/api/response/cancelled-invoices/audit-cancelled-invoices-report-entry.model';
import { Router } from '@angular/router';
import { NotificationService } from '../../../core';

@Component({
  selector: 'app-cancelled-invoices',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, Button, DragAndDropArea, MatIconModule],
  templateUrl: './cancelled-invoices.html',
  styleUrl: './cancelled-invoices.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CancelledInvoices implements OnInit {
  private cdr: ChangeDetectorRef = inject(ChangeDetectorRef);
  private loadingService = inject(LoadingService);
  private auditCancelledInvoicesService = inject(AuditCancelledInvoicesService);
  private router = inject(Router);
  private notificationService = inject(NotificationService);

  selectedPath = signal<string | null>(null);

  livroEntradaPath: string | null = null;
  livroSaidaPath: string | null = null;
  livroFiscalPath: string | null = null;
  notasCanceladasPath: string | null = null;
  auditHistory: AuditCancelledInvoicesReportEntry[] = [];

  currentPage = signal(1);
  pageSize = 5;

  get paginatedAudits(): AuditCancelledInvoicesReportEntry[] {
    const start = (this.currentPage() - 1) * this.pageSize;
    return this.auditHistory.slice(start, start + this.pageSize);
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.auditHistory.length / this.pageSize));
  }

  nextPage(): void {
    if (this.currentPage() < this.totalPages) {
      this.currentPage.update((p) => p + 1);
      this.cdr.markForCheck();
    }
  }

  previousPage(): void {
    if (this.currentPage() > 1) {
      this.currentPage.update((p) => p - 1);
      this.cdr.markForCheck();
    }
  }

  ngOnInit(): void {
    this.loadAllAudits();
  }

  onFilesValidated(event: { livroEntrada: string | null; livroSaida: string | null; notasCanceladas: string | null }) {
    this.livroEntradaPath = event.livroEntrada;
    this.livroSaidaPath = event.livroSaida;
    this.notasCanceladasPath = event.notasCanceladas;
    this.livroFiscalPath = this.livroEntradaPath ?? this.livroSaidaPath;
    this.cdr.markForCheck();
  }

  get isLoading() {
    return this.loadingService.isLoading;
  }

  executar() {
    this.loadingService.show();
    this.auditCancelledInvoicesService
      .run(this.livroFiscalPath!, this.notasCanceladasPath!)
      .subscribe({
        next: (response) => {
          const fileName = response.report_path.split('/').pop();
          console.log(fileName);
          this.router.navigate(['/taxdata/cancelled-invoices/report-details', fileName]);
          this.loadingService.hide();
        },
        error: (error) => {
          this.loadingService.hide();
          console.error(error);
        },
      });
  }

  verDetalhamento(audit: AuditCancelledInvoicesReportEntry): void {
    this.router.navigate(['/taxdata/cancelled-invoices/report-details', audit.file_name]);
  }

  excluirAuditoria(audit: AuditCancelledInvoicesReportEntry): void {
    this.notificationService.confirm(
      'Excluir auditoria',
      'Tem certeza que deseja excluir a auditoria?',
      () => this.deleteAudit(audit.file_name),
    );
  }

  trackByReportPath(_: number, audit: AuditCancelledInvoicesReportEntry): string {
    return audit.report_path;
  }

  prepareAuditDate(dateStr: string): Date {
    const [datePart, timePart] = dateStr.split(' ');
    const [day, month, year] = datePart.split('/');

    // Re-assemble into ISO format: YYYY-MM-DDTHH:mm:ss
    return new Date(`${year}-${month}-${day}T${timePart}`);
  }

  private loadAllAudits(): void {
    this.loadingService.show();
    this.auditCancelledInvoicesService.getAllAudits().subscribe({
      next: (audits) => {
        this.auditHistory = audits;
        if (this.currentPage() > this.totalPages && this.totalPages > 0) {
          this.currentPage.set(this.totalPages);
        } else if (this.auditHistory.length === 0) {
          this.currentPage.set(1);
        }
        this.loadingService.hide();
        this.cdr.markForCheck();
      },
      error: (error) => {
        this.loadingService.hide();
        console.error(error);
      },
    });
  }

  private deleteAudit(fileName: string): void {
    this.loadingService.show();
    this.auditCancelledInvoicesService.deleteAuditByFileName(fileName).subscribe({
      next: () => {
        this.loadingService.hide();
        this.loadAllAudits();
      },
      error: (error) => {
        this.loadingService.hide();
        console.error(error);
      },
    });
  }
}
