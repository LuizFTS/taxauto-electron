import { Component, ChangeDetectionStrategy, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  FormArray,
  FormControl,
} from '@angular/forms';
import { ModalService } from '../../core';
import { FiliaisModal } from './components/filiais-modal/filiais-modal';
import { Button, Select } from '../../shared';

@Component({
  selector: 'app-livros-fiscais',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, Button, Select],
  templateUrl: './livros-fiscais.html',
  styleUrl: './livros-fiscais.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LivrosFiscais implements OnInit {
  private fb = inject(FormBuilder);
  private modalService = inject(ModalService);

  tiposLivro = [
    { value: 1, label: 'Entrada' },
    { value: 2, label: 'Saída' },
  ];
  tarefasDisponiveis = [
    { id: 'atualizar', nome: 'Atualizar livro' },
    { id: 'abrir', nome: 'Abrir livro' },
    { id: 'fechar', nome: 'Fechar livro' },
    { id: 'salvar_excel', nome: 'Salvar planilha' },
    { id: 'salvar_pdf', nome: 'Salvar PDF' },
  ];

  startDate = '';
  endDate = '';
  endInput: HTMLInputElement | null = null;

  form: FormGroup = this.fb.group({
    tipoLivro: ['Entrada'],
    periodo: this.fb.group({
      start: [this.startDate],
      end: [this.endDate],
    }),
    tarefas: this.fb.array(this.tarefasDisponiveis.map(() => new FormControl(false))),
  });

  ngOnInit(): void {
    const today = new Date();

    // Today
    this.endDate = this.formatDate(today);
    this.form.get('periodo.end')?.setValue(this.endDate);

    // First day of the month
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    this.startDate = this.formatDate(firstDay);
    this.form.get('periodo.start')?.setValue(this.startDate);
  }

  get tarefasFormArray() {
    return this.form.controls['tarefas'] as FormArray;
  }

  isTarefaSelected(index: number): boolean {
    return this.tarefasFormArray.at(index).value;
  }

  toggleTarefa(index: number) {
    const currentValue = this.tarefasFormArray.at(index).value;
    this.tarefasFormArray.at(index).setValue(!currentValue);
  }

  executar() {
    const selectedTarefas = this.form.value.tarefas
      .map((checked: boolean, i: number) => (checked ? this.tarefasDisponiveis[i].id : null))
      .filter((v: string | null) => v !== null);

    const payload = {
      tipoLivro: this.form.value.tipoLivro,
      dataInicial: this.form.value.periodo.start,
      dataFinal: this.form.value.periodo.end,
      tarefas: selectedTarefas,
    };

    console.log('Executando com os parâmetros:', payload);
  }

  onStartInput(event: Event, end: HTMLInputElement): void {
    const value = (event.target as HTMLInputElement).value;

    if (value.length !== 10) return;

    const parsed = this.parseDate(value);
    if (!parsed) return;

    const lastDay = new Date(parsed.getFullYear(), parsed.getMonth() + 1, 0);
    const formattedLastDay = this.formatDate(lastDay);
    this.form.get('periodo.end')?.setValue(formattedLastDay);

    end.focus();
    setTimeout(() => end.select(), 0);
  }

  onDateInput(event: Event): void {
    const input = event.target as HTMLInputElement;

    let value = input.value.replace(/\D/g, '');

    value = value.substring(0, 8);

    if (value.length > 4) {
      value = value.replace(/(\d{2})(\d{2})(\d+)/, '$1/$2/$3');
    } else if (value.length > 2) {
      value = value.replace(/(\d{2})(\d+)/, '$1/$2');
    }

    input.value = value;
  }

  openFiliaisModal() {
    console.log('openFiliaisModal');
    this.modalService.open({
      component: FiliaisModal,
      data: {
        title: 'Seleção de filiais',
        subtitle: 'Selecione os grupos ou filiais individuais para execução',
        onConfirm: (branches: string[]) => {
          console.log('Selected branches from modal:', branches);
        },
      } as Partial<FiliaisModal>,
    });
  }

  private formatDate(date: Date): string {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();

    return `${day}/${month}/${year}`;
  }

  private parseDate(value: string): Date | null {
    const [day, month, year] = value.split('/').map(Number);

    const date = new Date(year, month - 1, day);

    // valida se a data realmente existe
    if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
      return null;
    }

    return date;
  }
}
