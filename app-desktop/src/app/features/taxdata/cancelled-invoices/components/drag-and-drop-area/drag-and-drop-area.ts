import { Component, EventEmitter, Output, inject, NO_ERRORS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DragAndDrop } from '../../../../../shared/components/drag-and-drop/drag-and-drop';
import { TaxReportsService } from '../../../../../core/services/api/automation/tax-reports.service';
import { NotificationService } from '../../../../../core/services/notification.service';
import { Card } from '../../../../../shared';

interface MappedFile {
  originalPath: string;
  name: string;
  sizeStr: string;
  statusText: string;
  isValid: boolean;
}

@Component({
  selector: 'app-drag-and-drop-area',
  imports: [CommonModule, DragAndDrop, Card],
  templateUrl: './drag-and-drop-area.html',
  styleUrl: './drag-and-drop-area.scss',
  schemas: [NO_ERRORS_SCHEMA],
})
export class DragAndDropArea {
  private taxReportsService = inject(TaxReportsService);
  private notificationService = inject(NotificationService);

  @Output() filesValidated = new EventEmitter<{
    livroEntrada: string | null;
    livroSaida: string | null;
    notasCanceladas: string | null;
  }>();

  livroEntradaMappedFile: MappedFile | null = null;
  livroSaidaMappedFile: MappedFile | null = null;
  notasCanceladasMappedFile: MappedFile | null = null;

  livroEntradaLoading = false;
  livroSaidaLoading = false;
  notasCanceladasLoading = false;

  onLivroEntradaDropped(files: string[]) {
    if (!files.length) return;
    const filePath = files[0];
    this.livroEntradaMappedFile = null;
    this.livroEntradaLoading = true;

    this.taxReportsService
      .validateCancelledInvoiceFile({ file_path: filePath, file_type: 'livro_fiscal' })
      .subscribe({
        next: (res) => {
          this.livroEntradaLoading = false;
          this.livroEntradaMappedFile = {
            originalPath: filePath,
            name: this.getFileName(filePath),
            sizeStr: 'Pronto para processar',
            statusText: res.is_valid
              ? `Arquivo OK: ${res.record_count} registros identificados`
              : res.message,
            isValid: res.is_valid,
          };
          this.checkOverallValidity();
        },
        error: () => {
          this.livroEntradaLoading = false;
          this.livroEntradaMappedFile = {
            originalPath: filePath,
            name: this.getFileName(filePath),
            sizeStr: 'Erro na leitura',
            statusText: 'Falha ao comunicar com o servidor',
            isValid: false,
          };
        },
      });
  }

  onLivroSaidaDropped(files: string[]) {
    if (!files.length) return;
    const filePath = files[0];
    this.livroSaidaMappedFile = null;
    this.livroSaidaLoading = true;

    this.taxReportsService
      .validateCancelledInvoiceFile({ file_path: filePath, file_type: 'livro_fiscal' })
      .subscribe({
        next: (res) => {
          this.livroSaidaLoading = false;
          this.livroSaidaMappedFile = {
            originalPath: filePath,
            name: this.getFileName(filePath),
            sizeStr: 'Pronto para processar',
            statusText: res.is_valid
              ? `Arquivo OK: ${res.record_count} registros identificados`
              : res.message,
            isValid: res.is_valid,
          };
          this.checkOverallValidity();
        },
        error: () => {
          this.livroSaidaLoading = false;
          this.livroSaidaMappedFile = {
            originalPath: filePath,
            name: this.getFileName(filePath),
            sizeStr: 'Erro na leitura',
            statusText: 'Falha ao comunicar com o servidor',
            isValid: false,
          };
        },
      });
  }

  onNotasCanceladasDropped(files: string[]) {
    if (!files.length) return;
    const filePath = files[0];
    this.notasCanceladasMappedFile = null;
    this.notasCanceladasLoading = true;

    this.taxReportsService
      .validateCancelledInvoiceFile({ file_path: filePath, file_type: 'notas_canceladas' })
      .subscribe({
        next: (res) => {
          this.notasCanceladasLoading = false;
          this.notasCanceladasMappedFile = {
            originalPath: filePath,
            name: this.getFileName(filePath),
            sizeStr: 'Pronto para processar',
            statusText: res.is_valid
              ? `Arquivo OK: ${res.record_count} registros identificados`
              : res.message,
            isValid: res.is_valid,
          };
          this.checkOverallValidity();
        },
        error: () => {
          this.notasCanceladasLoading = false;
          this.notasCanceladasMappedFile = {
            originalPath: filePath,
            name: this.getFileName(filePath),
            sizeStr: 'Erro na leitura',
            statusText: 'Falha ao comunicar com o servidor',
            isValid: false,
          };
        },
      });
  }

  onLivroEntradaRemoved() {
    this.livroEntradaMappedFile = null;
    this.checkOverallValidity();
  }

  onLivroSaidaRemoved() {
    this.livroSaidaMappedFile = null;
    this.checkOverallValidity();
  }

  onNotasCanceladasRemoved() {
    this.notasCanceladasMappedFile = null;
    this.checkOverallValidity();
  }

  private checkOverallValidity() {
    this.filesValidated.emit({
      livroEntrada: this.livroEntradaMappedFile?.isValid
        ? this.livroEntradaMappedFile.originalPath
        : null,
      livroSaida: this.livroSaidaMappedFile?.isValid
        ? this.livroSaidaMappedFile.originalPath
        : null,
      notasCanceladas: this.notasCanceladasMappedFile?.isValid
        ? this.notasCanceladasMappedFile.originalPath
        : null,
    });
  }

  private getFileName(filePath: string): string {
    return filePath.split(/[/\\]/).pop() || filePath;
  }
}
