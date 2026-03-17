import {
  ChangeDetectorRef,
  Component,
  ChangeDetectionStrategy,
  inject,
  OnInit,
  signal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  FormArray,
  FormControl,
} from '@angular/forms';
import { ModalService, NotificationService } from '../../core';
import { FiliaisModal } from './components/filiais-modal/filiais-modal';
import { Button, Select } from '../../shared';
import { LivrosFiscaisService } from '../../core/services/api/automation/livros-fiscais.service';

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
  private livrosFiscaisService = inject(LivrosFiscaisService);
  private cdr: ChangeDetectorRef = inject(ChangeDetectorRef);
  private notificationService = inject(NotificationService);

  selectedPath = signal<string | null>(null);

  tiposLivro = [
    { value: 1, label: 'Entrada' },
    { value: 2, label: 'Saída' },
  ];
  tarefasDisponiveis = [
    { id: 'atualizar', nome: 'Atualizar livro' },
    { id: 'abrir', nome: 'Abrir livro' },
    { id: 'fechar', nome: 'Fechar livro' },
    { id: 'salvar_excel', nome: 'Salvar Excel' },
    { id: 'salvar_pdf', nome: 'Salvar PDF' },
  ];

  startDate = '';
  endDate = '';
  endInput: HTMLInputElement | null = null;
  selectedFiliais: string[] = [];

  form: FormGroup = this.fb.group({
    tipoLivro: [],
    periodo: this.fb.group({
      start: [this.startDate],
      end: [this.endDate],
    }),
    consolidado: [false],
    tarefas: this.fb.array(this.tarefasDisponiveis.map(() => new FormControl(false))),
  });

  getConsolidadoControl(): FormControl {
    return this.form.get('consolidado') as FormControl;
  }

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
    const control = this.tarefasFormArray.at(index);
    const newValue = !control.value;
    control.setValue(newValue);

    if (index === 3 && newValue === false) {
      this.form.get('consolidado')?.setValue(false);
    }
  }

  async executar() {
    console.log(this.form.value);
    const selectedTarefas = this.form.value.tarefas
      .map((checked: boolean, i: number) => (checked ? this.tarefasDisponiveis[i].id : null))
      .filter((v: string | null) => v !== null);

    if (selectedTarefas.length === 0) {
      this.notificationService.alert('Atenção!', 'Selecione pelo menos uma tarefa para executar.');
      return;
    }

    if (!this.form.value.periodo.start || !this.form.value.periodo.end) {
      this.notificationService.alert('Atenção!', 'Selecione o período de execução.');
      return;
    }

    if (this.selectedFiliais.length === 0) {
      this.notificationService.alert('Atenção!', 'Selecione pelo menos uma filial para executar.');
      return;
    }

    if (this.form.value.tipoLivro === null) {
      this.notificationService.alert('Atenção!', 'Selecione o tipo de livro.');
      return;
    }

    if (selectedTarefas.includes('salvar_excel') || selectedTarefas.includes('salvar_pdf')) {
      const path = await this.pickFolder();
      if (!path) {
        this.notificationService.alert('Atenção!', 'Selecione a pasta de destino.');
        return;
      }
    }

    const payload = {
      book_type: this.form.value.tipoLivro === 1 ? 'entrada' : 'saida',
      start_date: this.form.value.periodo.start,
      end_date: this.form.value.periodo.end,
      filiais: this.selectedFiliais,
      consolidado: this.form.value.consolidado,
      save_path: this.selectedPath() || null,
      tasks: {
        open_book: selectedTarefas.includes('abrir'),
        update_book: selectedTarefas.includes('atualizar'),
        close_book: selectedTarefas.includes('fechar'),
        save_spreadsheet: selectedTarefas.includes('salvar_excel'),
        save_pdf: selectedTarefas.includes('salvar_pdf'),
      },
    };

    try {
      this.livrosFiscaisService.execute(payload).subscribe({
        next: () => {
          this.notificationService.success('Sucesso!', 'Processo concluído!');
          window.electron.focusWindow();
        },
        error: (error) => {
          if (error.error.code === 'AUTOMATION_STOPPED') {
            this.notificationService.alert('Atenção!', 'Processo interrompido.');
            window.electron.focusWindow();
            return;
          }
          this.notificationService.error('Erro!', error.error.detail);
          window.electron.focusWindow();
        },
      });
    } catch (error) {
      this.notificationService.error('Erro!', 'Erro ao executar tarefas.');
      console.log(error);
    }
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
    this.modalService.open({
      component: FiliaisModal,
      data: {
        title: 'Seleção de filiais',
        subtitle: 'Selecione os grupos ou filiais individuais para execução',
        onConfirm: (branches: string[]) => {
          this.selectedFiliais = [...branches];
          this.cdr.detectChanges();
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

  private async pickFolder(): Promise<string | null> {
    try {
      const path = await window.electron.invoke('select-directory', null);

      if (path) {
        this.selectedPath.set(path);
        return path;
      }
      return null;
    } catch (error) {
      this.notificationService.error('Erro!', 'Erro ao selecionar pasta');
      console.error(error);
      return null;
    }
  }
}
