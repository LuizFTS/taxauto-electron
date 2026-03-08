import { Component, inject, OnInit } from '@angular/core';
import { CommonModule, CurrencyPipe } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ApuracaoApiService, ApuracaoFilial } from '../../../../core';

@Component({
  selector: 'app-resultado',
  standalone: true,
  imports: [CommonModule, CurrencyPipe],
  templateUrl: './resultado.html',
  styleUrl: './resultado.scss',
})
export class Resultado implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private api = inject(ApuracaoApiService);

  periodoId!: number;
  resultados: ApuracaoFilial[] = [];
  carregando = false;
  exportando = false;
  filialDetalhe: ApuracaoFilial | null = null;

  get totalRecolher(): number {
    return this.resultados.reduce((s, r) => s + r.icms_a_recolher, 0);
  }

  get totalCredores(): number {
    return this.resultados.filter((r) => r.saldo_credor > 0).length;
  }

  ngOnInit(): void {
    this.periodoId = Number(this.route.snapshot.paramMap.get('id'));
    this.carregarResultados();
  }

  carregarResultados(): void {
    this.carregando = true;
    this.api.listarResultados(this.periodoId).subscribe({
      next: (r) => {
        this.resultados = r;
        this.carregando = false;
      },
      error: () => {
        this.carregando = false;
      },
    });
  }

  verDetalhe(filial: ApuracaoFilial): void {
    this.filialDetalhe = filial;
  }

  fecharDetalhe(): void {
    this.filialDetalhe = null;
  }

  exportar(): void {
    this.exportando = true;
    this.api.exportarResultado(this.periodoId).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `apuracao_${this.periodoId}.xlsx`;
        a.click();
        URL.revokeObjectURL(url);
        this.exportando = false;
      },
      error: () => {
        this.exportando = false;
      },
    });
  }

  novaApuracao(): void {
    this.router.navigate(['/apuracao']);
  }

  trackByCodigo(_: number, r: ApuracaoFilial): string {
    return r.filial_codigo;
  }
}
