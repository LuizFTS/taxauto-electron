import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, switchMap, takeWhile, startWith } from 'rxjs';
import { CriarPeriodoResponse } from '../../models/criar-periodo-response.model';
import { ArquivoFiscal } from '../../models/arquivo-fiscal.model';
import { ApuracaoFilial } from '../../models/apuracao-filial.model';
import type { Periodo } from '../../models/periodo.model';
import type { ProcessamentoStatus } from '../../models/processamento-status.model';
import { BackendService } from './backend.service';

@Injectable({ providedIn: 'root' })
export class ApuracaoApiService {
  private http = inject(HttpClient);
  private backend = inject(BackendService);

  // ── Períodos ──────────────────────────────────────────────────────────────

  listarPeriodos(): Observable<Periodo[]> {
    return this.http.get<Periodo[]>(`${this.backend.api}/periodos/`);
  }

  criarPeriodo(ano: number, mes: number): Observable<CriarPeriodoResponse> {
    return this.http.post<CriarPeriodoResponse>(`${this.backend.api}/periodos/`, { ano, mes });
  }

  buscarPeriodo(id: number): Observable<Periodo> {
    return this.http.get<Periodo>(`${this.backend.api}/periodos/${id}`);
  }

  // ── Arquivos ──────────────────────────────────────────────────────────────

  listarArquivos(periodoId: number): Observable<ArquivoFiscal[]> {
    return this.http.get<ArquivoFiscal[]>(`${this.backend.api}/periodos/${periodoId}/arquivos`);
  }

  validarArquivos(periodoId: number): Observable<ArquivoFiscal[]> {
    return this.http.post<ArquivoFiscal[]>(
      `${this.backend.api}/periodos/${periodoId}/arquivos/validar`,
      {},
    );
  }

  // ── Apuração ──────────────────────────────────────────────────────────────

  executarApuracao(periodoId: number): Observable<{ job_id: string }> {
    return this.http.post<{ job_id: string }>(
      `${this.backend.api}/periodos/${periodoId}/executar`,
      {},
    );
  }

  /** Poll do status de processamento a cada 1s até concluir */
  acompanharProcessamento(periodoId: number): Observable<ProcessamentoStatus> {
    return interval(1000).pipe(
      startWith(0),
      switchMap(() =>
        this.http.get<ProcessamentoStatus>(`${this.backend.api}/periodos/${periodoId}/status`),
      ),
      takeWhile((s) => !s.concluido && !s.erro, true),
    );
  }

  listarResultados(periodoId: number): Observable<ApuracaoFilial[]> {
    return this.http.get<ApuracaoFilial[]>(`${this.backend.api}/periodos/${periodoId}/resultado`);
  }

  exportarResultado(periodoId: number): Observable<Blob> {
    return this.http.get(`${this.backend.api}/periodos/${periodoId}/resultado/exportar`, {
      responseType: 'blob',
    });
  }
}
