import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, interval, switchMap, takeWhile, startWith } from 'rxjs';
import { Periodo, CriarPeriodoResponse } from '../models/periodo.model';
import { ArquivoFiscal } from '../models/arquivo-fiscal.model';
import { ApuracaoFilial, ProcessamentoStatus } from '../models/apuracao-resultado.model';

const API = 'http://127.0.0.1:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class ApuracaoApiService {
  constructor(private http: HttpClient) {}

  // ── Períodos ──────────────────────────────────────────────────────────────

  listarPeriodos(): Observable<Periodo[]> {
    return this.http.get<Periodo[]>(`${API}/periodos/`);
  }

  criarPeriodo(ano: number, mes: number): Observable<CriarPeriodoResponse> {
    return this.http.post<CriarPeriodoResponse>(`${API}/periodos/`, { ano, mes });
  }

  buscarPeriodo(id: number): Observable<Periodo> {
    return this.http.get<Periodo>(`${API}/periodos/${id}`);
  }

  // ── Arquivos ──────────────────────────────────────────────────────────────

  listarArquivos(periodoId: number): Observable<ArquivoFiscal[]> {
    return this.http.get<ArquivoFiscal[]>(`${API}/periodos/${periodoId}/arquivos`);
  }

  validarArquivos(periodoId: number): Observable<ArquivoFiscal[]> {
    return this.http.post<ArquivoFiscal[]>(`${API}/periodos/${periodoId}/arquivos/validar`, {});
  }

  // ── Apuração ──────────────────────────────────────────────────────────────

  executarApuracao(periodoId: number): Observable<{ job_id: string }> {
    return this.http.post<{ job_id: string }>(`${API}/periodos/${periodoId}/executar`, {});
  }

  /** Poll do status de processamento a cada 1s até concluir */
  acompanharProcessamento(periodoId: number): Observable<ProcessamentoStatus> {
    return interval(1000).pipe(
      startWith(0),
      switchMap(() => this.http.get<ProcessamentoStatus>(`${API}/periodos/${periodoId}/status`)),
      takeWhile((s) => !s.concluido && !s.erro, true),
    );
  }

  listarResultados(periodoId: number): Observable<ApuracaoFilial[]> {
    return this.http.get<ApuracaoFilial[]>(`${API}/periodos/${periodoId}/resultado`);
  }

  exportarResultado(periodoId: number): Observable<Blob> {
    return this.http.get(`${API}/periodos/${periodoId}/resultado/exportar`, {
      responseType: 'blob',
    });
  }
}
