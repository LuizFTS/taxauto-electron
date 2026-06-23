import {
  ChangeDetectorRef,
  Component,
  ChangeDetectionStrategy,
  inject,
  signal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormArray, FormGroup } from '@angular/forms';

import { ModalService, NotificationService } from '../../../core';
import { SelectBranchesModal } from '../../../shared/components/select-branches-modal/select-branches-modal';
import { Button, Select, Card } from '../../../shared';
import { TaxReportsService } from '../../../core/services/api/automation/tax-reports.service';

import {
  TIPOS_RELATORIO,
  TAREFAS_DISPONIVEIS,
  TAREFAS_COM_DESTINO,
  TIPOS_RELATORIO_COM_DESTINO,
  TIPOS_OPERACAO,
  TIPOS_DOCUMENTO,
  TAREFAS_PORTALGED,
} from './livros-fiscais.constants';
import {
  LivroFiscalPayload,
  TarefaId,
  type CancelledInvoicesPayload,
  type DownloadXmlsPayload,
} from './livros-fiscais.types';
import { buildLivrosFiscaisForm, getSelectedTarefas } from './livros-fiscais.form';
import { applyDateMask, formatDate, lastDayOfMonth, parseDate } from './livros-fiscais.utils';
import { LoadingService } from '../../../core/services/loading.service';
import { Router } from '@angular/router';
import { DownloadXmlsService } from '../../../core/services/api/automation/download-xmls.service';

@Component({
  selector: 'app-livros-fiscais',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, Button, Select, Card],
  templateUrl: './livros-fiscais.html',
  styleUrl: './livros-fiscais.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LivrosFiscais {
  private fb = inject(FormBuilder);
  private modalService = inject(ModalService);
  private taxReportsService = inject(TaxReportsService);
  private downloadXmlsService = inject(DownloadXmlsService);
  private cdr = inject(ChangeDetectorRef);
  private notificationService = inject(NotificationService);
  private loadingService = inject(LoadingService);
  private router = inject(Router);

  readonly tiposRelatorio = TIPOS_RELATORIO;
  readonly tiposOperacao = TIPOS_OPERACAO;
  readonly tiposDocumento = TIPOS_DOCUMENTO;
  readonly tarefasDisponiveis = TAREFAS_DISPONIVEIS;

  selectedPath = signal<string | null>(null);
  selectedFiliais: string[] = [];

  form: FormGroup = buildLivrosFiscaisForm(this.fb);

  get tarefasFormArray(): FormArray {
    return this.form.controls['tarefas'] as FormArray;
  }

  isTarefaSelected(index: number): boolean {
    return this.tarefasFormArray.at(index).value;
  }

  toggleTarefa(index: number): void {
    const control = this.tarefasFormArray.at(index);
    control.setValue(!control.value);
  }

  onDateInput(event: Event): void {
    applyDateMask(event.target as HTMLInputElement);
  }

  onStartInput(event: Event, endInput: HTMLInputElement): void {
    const value = (event.target as HTMLInputElement).value;
    if (value.length !== 10) return;

    const parsed = parseDate(value);
    if (!parsed) return;

    this.form.get('periodo.end')?.setValue(formatDate(lastDayOfMonth(parsed)));
    endInput.focus();
    setTimeout(() => endInput.select(), 0);
  }

  openFiliaisModal(): void {
    this.modalService.open({
      component: SelectBranchesModal,
      data: {
        title: 'Seleção de filiais',
        subtitle: 'Selecione os grupos ou filiais individuais para execução',
        filiais: this.selectedFiliais,
        onConfirm: (branches: string[]) => {
          this.selectedFiliais = [...branches];
          this.cdr.detectChanges();
        },
      } as Partial<SelectBranchesModal>,
    });
  }

  async executar(): Promise<void> {
    if (!this.validarFormulario()) return;

    this.loadingService.show();

    const selectedTarefas = getSelectedTarefas(this.form) as TarefaId[];
    const precisaDestino =
      selectedTarefas.some((t) => TAREFAS_COM_DESTINO.has(t)) ||
      TIPOS_RELATORIO_COM_DESTINO.has(this.form.value.tipoLivro);

    if (precisaDestino) {
      const path = await this.pickFolder();
      if (!path) {
        this.finalizarComAlerta('Selecione a pasta de destino.');
        return;
      }
    }

    if (TAREFAS_PORTALGED.has(this.form.value.tipoLivro)) {
      if (this.form.value.lembrarSenha) {
        localStorage.setItem('portalged_login', this.form.value.login);
        localStorage.setItem('portalged_senha', this.form.value.senha);
        localStorage.setItem('portalged_lembrar', 'true');
      } else {
        localStorage.removeItem('portalged_login');
        localStorage.removeItem('portalged_senha');
        localStorage.removeItem('portalged_lembrar');
      }

      switch (this.form.value.tipoLivro) {
        case 3:
          this.taxReportsService
            .generateCancelledInvoicesReport(this.buildPayloadCancelledInvoices())
            .subscribe({
              next: () => this.onSuccess(),
              error: (err) => this.onError(err),
            });
          return;
        case 4:
          this.downloadXmlsService.execute(this.buildPayloadDownloadXmls()).subscribe({
            next: () => this.onSuccess(),
            error: (err) => this.onError(err),
          });
          return;
        case 5:
          this.taxReportsService
            .generateCancelledInvoicesReportFlow(this.buildPayloadCancelledInvoices())
            .subscribe({
              next: (res) => {
                this.onSuccess();

                const fileName = res.report_path.split('/').pop();
                this.router.navigate(['/taxdata/cancelled-invoices/report-details', fileName]);
              },
              error: (err) => this.onError(err),
            });
          return;
        default:
          return;
      }
    }

    this.taxReportsService.execute(this.buildPayload(selectedTarefas)).subscribe({
      next: () => this.onSuccess(),
      error: (err) => this.onError(err),
    });
  }

  // ─── privados ────────────────────────────────────────────────────────────────

  private validarFormulario(): boolean {
    const selectedTarefas = getSelectedTarefas(this.form);
    const { start, end } = this.form.value.periodo;

    const bookType = this.form.value.tipoLivro;

    if (TAREFAS_PORTALGED.has(bookType) && (!this.form.value.login || !this.form.value.senha)) {
      return this.alerta('Informe o usuário e a senha para acessar o PortalGED.');
    }

    if (bookType === 4 && (!this.form.value.tipoDocumento || !this.form.value.tipoOperacao)) {
      return this.alerta('Informe o tipo de documento e operação.');
    }

    if (selectedTarefas.length === 0 && !TAREFAS_PORTALGED.has(bookType))
      return this.alerta('Selecione pelo menos uma tarefa para executar.');
    if (!start || !end) return this.alerta('Selecione o período de execução.');
    if (this.selectedFiliais.length === 0)
      return this.alerta('Selecione pelo menos uma filial para executar.');
    if (bookType === null) return this.alerta('Selecione o tipo de livro.');

    return true;
  }

  private buildPayload(selectedTarefas: TarefaId[]): LivroFiscalPayload {
    const { tipoLivro, periodo } = this.form.value;

    return {
      book_type: tipoLivro === 1 ? 'entrada' : 'saida',
      start_date: periodo.start,
      end_date: periodo.end,
      filiais: this.selectedFiliais,
      save_path: this.selectedPath() ?? null,
      tasks: {
        open_book: selectedTarefas.includes('abrir'),
        update_book: selectedTarefas.includes('atualizar'),
        close_book: selectedTarefas.includes('fechar'),
        save_spreadsheet: selectedTarefas.includes('salvar_excel'),
        save_pdf: selectedTarefas.includes('salvar_pdf'),
      },
    };
  }

  private buildPayloadCancelledInvoices(): CancelledInvoicesPayload {
    const { periodo, login, senha } = this.form.value;

    return {
      start_date: periodo.start,
      end_date: periodo.end,
      filiais: this.selectedFiliais,
      save_path: this.selectedPath()!,
      login: login,
      password: senha,
    };
  }
  private buildPayloadDownloadXmls(): DownloadXmlsPayload {
    const { periodo, login, senha, tipoDocumento, tipoOperacao } = this.form.value;

    return {
      start_date: periodo.start,
      end_date: periodo.end,
      filiais: this.selectedFiliais,
      save_path: this.selectedPath()!,
      login: login,
      password: senha,
      tipo_documento: tipoDocumento,
      tipo_operacao: tipoOperacao,
    };
  }

  private onSuccess(): void {
    this.loadingService.hide();
    this.notificationService.success('Sucesso!', 'Processo concluído!');
    window.electron.focusWindow();
    this.cdr.markForCheck();
  }

  private onError(error: { error: { code: string; detail: string } }): void {
    this.loadingService.hide();
    const isStopped = error?.error?.code === 'AUTOMATION_STOPPED';
    const msg = isStopped
      ? 'Processo interrompido.'
      : (error?.error?.detail ?? 'Erro ao executar tarefas.');
    const method = isStopped ? 'alert' : 'error';
    const title = isStopped ? 'Atenção!' : 'Erro!';

    this.notificationService[method](title, msg);
    window.electron.focusWindow();
    this.cdr.markForCheck();
  }

  private finalizarComAlerta(msg: string): void {
    this.loadingService.hide();
    this.notificationService.alert('Atenção!', msg);
    this.cdr.markForCheck();
  }

  private alerta(msg: string): false {
    this.notificationService.alert('Atenção!', msg);
    return false;
  }

  private async pickFolder(): Promise<string | null> {
    try {
      const path = await window.electron.invoke('select-directory', null);
      if (path && typeof path === 'string') {
        this.selectedPath.set(path);
        return path;
      }
      return null;
    } catch {
      this.notificationService.error('Erro!', 'Erro ao selecionar pasta');
      return null;
    }
  }

  get isLoading(): boolean {
    return this.loadingService.isLoading();
  }

  get TAREFAS_PORTALGED() {
    return TAREFAS_PORTALGED;
  }
}
