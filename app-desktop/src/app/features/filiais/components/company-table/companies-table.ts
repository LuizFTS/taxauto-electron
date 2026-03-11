import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import type { Empresa } from '../../../../core';

@Component({
  selector: 'app-companies-table',
  imports: [MatIconModule],
  templateUrl: './companies-table.html',
  styleUrl: './companies-table.scss',
})
export class CompaniesTable {
  @Input() isCreating = false;
  @Input() newRowData: Partial<Empresa> = {
    numero: '',
    nome: '',
    status: 'Ativo',
  };
  @Input() editingRows: Record<string, Partial<Empresa>> = {};
  @Input() empresas: Empresa[] | null = null;

  @Output() saveEdit = new EventEmitter<string>();
  @Output() startEdit = new EventEmitter<Empresa>();
  @Output() deleteRow = new EventEmitter<string>();
  @Output() updateEditField = new EventEmitter<{ id: string; field: string; event: Event }>();
  @Output() startCreate = new EventEmitter<void>();
  @Output() cancelCreate = new EventEmitter<void>();
  @Output() saveCreate = new EventEmitter<Empresa>();
  @Output() updateCreateField = new EventEmitter<{ field: string; event: Event }>();

  @Output() cancelEdit = new EventEmitter<string>();

  // ---- CRUD Operations ----

  startEditHandle(item: Empresa) {
    this.startEdit.emit(item);
  }

  cancelEditHandle(id: string) {
    this.cancelEdit.emit(id);
  }

  saveEditHandle(id: string) {
    this.saveEdit.emit(id);
  }

  deleteRowHandle(id: string) {
    this.deleteRow.emit(id);
  }

  updateEditFieldHandle(id: string, field: string, event: Event) {
    this.updateEditField.emit({ id, field, event });
  }

  // --- Create ---
  startCreateHandle() {
    this.startCreate.emit();
  }

  cancelCreateHandle() {
    this.cancelCreate.emit();
  }

  saveCreateHandle() {
    this.saveCreate.emit(this.newRowData as Empresa);
  }

  updateCreateFieldHandle(field: string, event: Event) {
    this.updateCreateField.emit({ field, event });
  }
}
