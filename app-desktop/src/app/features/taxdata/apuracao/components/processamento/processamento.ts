import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject, takeUntil } from 'rxjs';
import { ApuracaoApiService, ProcessamentoStatus } from '../../../../../core';

const ETAPAS_LABEL: Record<string, string> = {
  NORMALIZACAO: 'Normalizando dados',
  CLASSIFICACAO: 'Classificando operações fiscais',
  CALCULO: 'Calculando ICMS',
  CONSOLIDACAO: 'Consolidando por filial',
  RELATORIO: 'Gerando relatórios',
};

@Component({
  selector: 'app-processamento',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './processamento.html',
  styleUrls: ['./processamento.scss'],
})
export class Processamento implements OnInit, OnDestroy {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private api = inject(ApuracaoApiService);

  private destroy$ = new Subject<void>();

  periodoId!: number;
  status: ProcessamentoStatus | null = null;
  concluido = false;
  erro: string | null = null;

  readonly etapas = Object.entries(ETAPAS_LABEL).map(([key, label]) => ({ key, label }));

  ngOnInit(): void {
    this.periodoId = Number(this.route.snapshot.paramMap.get('id'));
    this.iniciarProcessamento();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private iniciarProcessamento(): void {
    // 1. Dispara o job
    this.api
      .executarApuracao(this.periodoId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => this.acompanharStatus(),
        error: (err) => {
          this.erro = err?.error?.detail ?? 'Erro ao iniciar processamento.';
        },
      });
  }

  private acompanharStatus(): void {
    this.api
      .acompanharProcessamento(this.periodoId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (s) => {
          this.status = s;
          if (s.concluido) {
            this.concluido = true;
            // Redireciona para resultado após 1.2s
            setTimeout(() => {
              this.router.navigate(['/apuracao/resultado', this.periodoId]);
            }, 1200);
          }
        },
        error: (err) => {
          this.erro = err?.error?.detail ?? 'Erro durante o processamento.';
        },
      });
  }

  voltarInicio(): void {
    this.router.navigate(['/apuracao']);
  }

  etapaAtiva(key: string): boolean {
    return this.status?.etapa === key;
  }

  etapaConcluida(key: string): boolean {
    const etapas = this.etapas.map((e) => e.key);
    const atualIdx = etapas.indexOf(this.status?.etapa ?? '');
    const testedIdx = etapas.indexOf(key);
    return this.concluido || (atualIdx > testedIdx && atualIdx !== -1);
  }
}
