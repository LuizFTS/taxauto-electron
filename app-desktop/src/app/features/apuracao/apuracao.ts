import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  ApuracaoApiService,
  Periodo,
  ArquivoFiscal,
  TipoArquivo,
  TIPOS_ARQUIVO_CONFIG,
} from '../../core';
import { PeriodoCriarModalComponent } from './components/periodo-criar-modal-component/periodo-criar-modal-component';

@Component({
  selector: 'app-apuracao',
  imports: [CommonModule, FormsModule, PeriodoCriarModalComponent],
  templateUrl: './apuracao.html',
  styleUrl: './apuracao.scss',
})
export class Apuracao implements OnInit, OnDestroy {
  private api = inject(ApuracaoApiService);
  private router = inject(Router);

  private destroy$ = new Subject<void>();

  // Estado do período
  periodos: Periodo[] = [];
  periodoSelecionado: Periodo | null = null;
  anoSelecionado: number = new Date().getFullYear();
  mesSelecionado: number = new Date().getMonth() + 1;

  // Estado dos arquivos
  arquivos: ArquivoFiscal[] = [];
  carregandoArquivos = false;
  validando = false;

  // Modal
  mostrarModalCriar = false;

  // UI
  carregandoPeriodos = false;
  podExecutar = false;

  readonly meses = [
    { valor: 1, label: 'Janeiro' },
    { valor: 2, label: 'Fevereiro' },
    { valor: 3, label: 'Março' },
    { valor: 4, label: 'Abril' },
    { valor: 5, label: 'Maio' },
    { valor: 6, label: 'Junho' },
    { valor: 7, label: 'Julho' },
    { valor: 8, label: 'Agosto' },
    { valor: 9, label: 'Setembro' },
    { valor: 10, label: 'Outubro' },
    { valor: 11, label: 'Novembro' },
    { valor: 12, label: 'Dezembro' },
  ];

  readonly anos = Array.from({ length: 6 }, (_, i) => new Date().getFullYear() - i);

  ngOnInit(): void {
    this.carregarPeriodos();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  // ── Períodos ──────────────────────────────────────────────────────────────

  carregarPeriodos(): void {
    this.carregandoPeriodos = true;
    this.api
      .listarPeriodos()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (periodos: Periodo[]) => {
          this.periodos = periodos;
          this.carregandoPeriodos = false;
          this.verificarPeriodoSelecionado();
        },
        error: () => {
          this.carregandoPeriodos = false;
        },
      });
  }

  private verificarPeriodoSelecionado(): void {
    const existente = this.periodos.find(
      (p) => p.ano === this.anoSelecionado && p.mes === this.mesSelecionado,
    );

    if (existente) {
      this.periodoSelecionado = existente;
      this.carregarArquivos();
    } else {
      this.periodoSelecionado = null;
      this.arquivos = [];
    }
  }

  onPeriodoChange(): void {
    this.verificarPeriodoSelecionado();
  }

  abrirModalCriar(): void {
    this.mostrarModalCriar = true;
  }

  onPeriodoCriado(periodo: Periodo): void {
    this.mostrarModalCriar = false;
    this.periodos = [periodo, ...this.periodos];
    this.periodoSelecionado = periodo;
    this.arquivos = this.gerarArquivosVazios();
    this.podExecutar = false;
  }

  onModalFechado(): void {
    this.mostrarModalCriar = false;
  }

  // ── Arquivos ──────────────────────────────────────────────────────────────

  carregarArquivos(): void {
    if (!this.periodoSelecionado?.id) return;
    this.carregandoArquivos = true;

    this.api
      .listarArquivos(this.periodoSelecionado.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (arquivos: ArquivoFiscal[]) => {
          this.arquivos = arquivos;
          this.carregandoArquivos = false;
          this.atualizarPodExecutar();
        },
        error: () => {
          this.arquivos = this.gerarArquivosVazios();
          this.carregandoArquivos = false;
        },
      });
  }

  validarArquivos(): void {
    if (!this.periodoSelecionado?.id) return;
    this.validando = true;

    this.api
      .validarArquivos(this.periodoSelecionado.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (arquivos: ArquivoFiscal[]) => {
          this.arquivos = arquivos;
          this.validando = false;
          this.atualizarPodExecutar();
        },
        error: () => {
          this.validando = false;
        },
      });
  }

  private gerarArquivosVazios(): ArquivoFiscal[] {
    return (
      Object.entries(TIPOS_ARQUIVO_CONFIG) as [
        TipoArquivo,
        { label: string; obrigatorio: boolean },
      ][]
    ).map(([tipo, config]) => ({
      tipo,
      label: config.label,
      nome_arquivo: null,
      caminho: null,
      status: 'AUSENTE' as const,
      obrigatorio: config.obrigatorio,
      erro_mensagem: null,
      total_linhas: null,
    }));
  }

  private atualizarPodExecutar(): void {
    const obrigatoriosFaltando = this.arquivos
      .filter((a) => a.obrigatorio)
      .some((a) => a.status === 'FAIL' || a.status === 'AUSENTE');

    this.podExecutar = !obrigatoriosFaltando && this.arquivos.some((a) => a.status === 'OK');
  }

  // ── Execução ──────────────────────────────────────────────────────────────

  executar(): void {
    if (!this.periodoSelecionado?.id || !this.podExecutar) return;
    this.router.navigate(['/apuracao/processamento', this.periodoSelecionado.id]);
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  get mesLabel(): string {
    return this.meses.find((m) => m.valor === this.mesSelecionado)?.label ?? '';
  }

  get arquivosObrigatorios(): ArquivoFiscal[] {
    return this.arquivos.filter((a) => a.obrigatorio);
  }

  get arquivosOpcionais(): ArquivoFiscal[] {
    return this.arquivos.filter((a) => !a.obrigatorio);
  }

  get totalOk(): number {
    return this.arquivos.filter((a) => a.status === 'OK').length;
  }

  get totalFail(): number {
    return this.arquivos.filter((a) => a.status === 'FAIL').length;
  }

  trackByTipo(_: number, a: ArquivoFiscal): string {
    return a.tipo;
  }
}
