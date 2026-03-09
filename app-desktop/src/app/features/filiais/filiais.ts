import { Component, ChangeDetectionStrategy, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { Button } from '../../shared/components/button/button';
import { MatIcon } from '@angular/material/icon';
import type { Empresa, Filial } from '../../core';

@Component({
  selector: 'app-filiais',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, Button, MatIcon],
  templateUrl: './filiais.html',
  styleUrl: './filiais.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class Filiais {
  activeTab: 'Empresas' | 'Filiais' = 'Empresas';

  filiais: Filial[] = [
    { id: '1', numero: '001', nome: 'FILIAL NORTE', uf: 'ES', empresaId: '1', status: 'Ativo' },
    { id: '2', numero: '002', nome: 'FILIAL SUL', uf: 'MG', empresaId: '1', status: 'Ativo' },
    {
      id: '3',
      numero: '001',
      nome: 'UNIDADE CENTRAL',
      uf: 'SP',
      empresaId: '2',
      status: 'Inativo',
    },
  ];

  // Mock Data
  empresas: Empresa[] = [
    { id: '1', numero: '001', nome: 'CASA DO ADUBO', filiais: [], status: 'Ativo' },
    { id: '2', numero: '002', nome: 'CASAL', filiais: [], status: 'Ativo' },
    { id: '3', numero: '003', nome: 'NUTRIEN', filiais: [], status: 'Inativo' },
  ];

  // Search
  searchQuery = '';

  // Inline Editing State Map (maps row id to editable object clone)
  editingRows: Record<string, Partial<Empresa | Filial>> = {};

  // Create Form State
  isCreating = false;
  newRowData: Partial<Empresa | Filial> = {};

  setActiveTab(tab: 'Empresas' | 'Filiais') {
    this.activeTab = tab;
    // reset edits when switching tabs
    this.editingRows = {};
    this.isCreating = false;
    this.searchQuery = '';
  }

  get filteredEmpresas(): Empresa[] {
    return this.empresas.filter(
      (e) =>
        e.nome.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        e.numero.includes(this.searchQuery),
    );
  }

  get filteredFiliais(): Filial[] {
    return this.filiais.filter(
      (f) =>
        f.nome.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        f.numero.includes(this.searchQuery),
    );
  }

  updateSearch(event: Event) {
    this.searchQuery = (event.target as HTMLInputElement).value;
  }

  // ---- CRUD Operations ----

  startEdit(item: Empresa | Filial) {
    this.editingRows[item.id] = { ...item };
  }

  cancelEdit(id: string) {
    delete this.editingRows[id];
  }

  saveEdit(id: string) {
    const editData = this.editingRows[id];

    if (this.activeTab === 'Empresas') {
      const idx = this.empresas.findIndex((e) => e.id === id);
      if (idx > -1) {
        this.empresas[idx] = { ...this.empresas[idx], ...(editData as Empresa) };
      }
    } else {
      const idx = this.filiais.findIndex((f) => f.id === id);
      if (idx > -1) {
        this.filiais[idx] = { ...this.filiais[idx], ...(editData as Filial) };
      }
    }

    delete this.editingRows[id];
  }

  deleteRow(id: string) {
    if (confirm('Tem certeza que deseja excluir?')) {
      if (this.activeTab === 'Empresas') {
        this.empresas = this.empresas.filter((e) => e.id !== id);
      } else {
        this.filiais = this.filiais.filter((f) => f.id !== id);
      }
    }
  }

  updateEditField(id: string, field: string, event: Event) {
    const target = event.target as HTMLInputElement | HTMLSelectElement;

    const row = this.editingRows[id] as Record<string, unknown>;
    row[field] = target.value;
  }

  // --- Create ---
  startCreate() {
    this.isCreating = true;
    this.newRowData = {
      id: Date.now().toString(),
      numero: '',
      nome: '',
      status: 'Ativo',
    };
    if (this.activeTab === 'Filiais') {
      (this.newRowData as Filial).empresaId = this.empresas.length > 0 ? this.empresas[0].id : '';
    }
  }

  cancelCreate() {
    this.isCreating = false;
    this.newRowData = {};
  }

  saveCreate() {
    if (!this.newRowData.numero || !this.newRowData.nome) return;

    if (this.activeTab === 'Empresas') {
      this.empresas = [...this.empresas, this.newRowData as Empresa];
    } else {
      this.filiais = [...this.filiais, this.newRowData as Filial];
    }

    this.isCreating = false;
    this.newRowData = {};
  }

  updateCreateField(field: string, event: Event) {
    const target = event.target as HTMLInputElement | HTMLSelectElement;

    const row = this.newRowData as Record<string, unknown>;
    row[field] = target.value;
  }
}
