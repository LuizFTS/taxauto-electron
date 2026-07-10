import { CommonModule } from '@angular/common';
import { Component, EventEmitter, inject, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ModalService } from '../../../core';

export interface FlowTask {
  id: string;
  code: string;
  label: string;
  checked: boolean;
}

@Component({
  selector: 'app-flow-tasks-modal',
  imports: [CommonModule, FormsModule],
  templateUrl: './flow-tasks-modal.html',
  styleUrl: './flow-tasks-modal.scss',
})
export class FlowTasksModal {
  private modalService = inject(ModalService);
  @Output() confirm = new EventEmitter<FlowTask[]>();
  @Output() cancelModal = new EventEmitter<void>();

  tasks: FlowTask[] = [
    { id: '1', code: 'atualizar-livro-saida', label: 'Atualizar livro de saída', checked: true },
    { id: '2', code: 'fechar-livro-saida', label: 'Fechar livro de saída', checked: true },
  ];

  get selectedCount(): number {
    return this.tasks.filter((t) => t.checked).length;
  }

  get allSelected(): boolean {
    return this.tasks.every((t) => t.checked);
  }

  toggleAll(): void {
    const target = !this.allSelected;
    this.tasks.forEach((t) => (t.checked = target));
  }

  clearAll(): void {
    this.tasks.forEach((t) => (t.checked = false));
  }

  onConfirm(): void {
    this.modalService.confirm(this.tasks.filter((t) => t.checked));
  }

  onCancel(): void {
    this.modalService.cancel();
  }
}
