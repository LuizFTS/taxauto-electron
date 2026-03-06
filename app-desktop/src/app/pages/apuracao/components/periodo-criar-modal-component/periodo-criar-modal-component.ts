import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApuracaoApiService } from '../../../../services/api.service';
import { Periodo } from '../../../../models/periodo.model';

const MESES = [
  'Janeiro',
  'Fevereiro',
  'Março',
  'Abril',
  'Maio',
  'Junho',
  'Julho',
  'Agosto',
  'Setembro',
  'Outubro',
  'Novembro',
  'Dezembro',
];

@Component({
  selector: 'app-periodo-criar-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './periodo-criar-modal-component.html',
  styleUrls: ['./periodo-criar-modal-component.scss'],
})
export class PeriodoCriarModalComponent implements OnInit {
  @Input() ano!: number;
  @Input() mes!: number;

  @Output() periodoCreated = new EventEmitter<Periodo>();
  @Output() closed = new EventEmitter<void>();

  criando = false;
  erro: string | null = null;
  workspacePath = '';

  ngOnInit(): void {
    // Preview do caminho que será criado
    this.workspacePath = `Documentos\\Apuracao_ICMS\\${this.ano}\\${String(this.mes).padStart(2, '0')}`;
  }

  get mesLabel(): string {
    return MESES[this.mes - 1] ?? '';
  }

  constructor(private api: ApuracaoApiService) {}

  criar(): void {
    this.criando = true;
    this.erro = null;

    this.api.criarPeriodo(this.ano, this.mes).subscribe({
      next: (res) => {
        this.criando = false;
        this.periodoCreated.emit(res.periodo);
      },
      error: (err) => {
        this.criando = false;
        this.erro = err?.error?.detail ?? 'Erro ao criar período. Tente novamente.';
      },
    });
  }

  fechar(): void {
    this.closed.emit();
  }
}
