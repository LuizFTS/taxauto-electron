import {
  Component,
  ChangeDetectionStrategy,
  CUSTOM_ELEMENTS_SCHEMA,
  inject,
  type OnInit,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Button } from '../../shared/components/button/button';
import { MatIcon } from '@angular/material/icon';
import type { Empresa, Filial } from '../../core';
import { BranchService } from '../../core/services/api/data/branch.service';
import { CompanyService } from '../../core/services/api/data/company.service';
import { CompanyMapper } from '../../shared/mappers/company.mapper';
import { BehaviorSubject, combineLatest, map, switchMap, type Observable } from 'rxjs';

@Component({
  selector: 'app-filiais',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, Button, MatIcon, FormsModule],
  templateUrl: './filiais.html',
  styleUrl: './filiais.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class Filiais implements OnInit {
  private branchService = inject(BranchService);
  private companyService = inject(CompanyService);

  activeTab: 'Empresas' | 'Filiais' = 'Empresas';

  private empresasSubject = new BehaviorSubject<Empresa[]>([]);
  private filiaisSubject = new BehaviorSubject<Filial[]>([]);

  empresasFiltered$!: Observable<Empresa[]>;
  filiaisFiltered$!: Observable<Filial[]>;

  // Search
  private searchSubject = new BehaviorSubject<string>('');
  searchQuery = '';

  // Inline Editing State Map
  editingRows: Record<string, Partial<Empresa | Filial>> = {};

  // Create Form State
  isCreating = false;
  newRowData: Partial<Empresa | Filial> = {};

  ngOnInit() {
    this.companyService
      .getAll()
      .pipe(
        switchMap((companies) =>
          this.branchService.getAll().pipe(map((branches) => ({ companies, branches }))),
        ),
      )
      .subscribe(({ companies, branches }) => {
        this.empresasSubject.next(CompanyMapper.toEmpresaList(companies, branches));
        this.filiaisSubject.next(CompanyMapper.toFilialList(branches, companies));
      });

    this.empresasFiltered$ = combineLatest([this.empresasSubject, this.searchSubject]).pipe(
      map(([list, q]) => list.filter((e) => e.nome.toLowerCase().includes(q.toLowerCase()))),
    );

    this.filiaisFiltered$ = combineLatest([this.filiaisSubject, this.searchSubject]).pipe(
      map(([list, q]) => list.filter((f) => f.nome.toLowerCase().includes(q.toLowerCase()))),
    );
  }

  setActiveTab(tab: 'Empresas' | 'Filiais') {
    this.activeTab = tab;
    this.editingRows = {};
    this.isCreating = false;
    this.searchQuery = '';
    this.searchSubject.next('');
  }

  onSearchChange(valor: string) {
    this.searchSubject.next(valor);
  }

  /** Lookup a parent company name by its ID from the raw (unfiltered) subject */
  getEmpresaNome(empresaId: string): string {
    const empresa = this.empresasSubject.value.find((e) => e.id === empresaId);
    return empresa?.nome ?? '—';
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
      const listaAtual = this.empresasSubject.value;
      const idx = listaAtual.findIndex((e) => e.id === id);
      if (idx > -1) {
        listaAtual[idx] = { ...listaAtual[idx], ...(editData as Empresa) };
        this.empresasSubject.next([...listaAtual]);
      }
    } else {
      const listaAtual = this.filiaisSubject.value;
      const idx = listaAtual.findIndex((f) => f.id === id);
      if (idx > -1) {
        listaAtual[idx] = { ...listaAtual[idx], ...(editData as Filial) };
        this.filiaisSubject.next([...listaAtual]);
      }
    }
    delete this.editingRows[id];
  }

  deleteRow(id: string) {
    if (confirm('Tem certeza que deseja excluir?')) {
      if (this.activeTab === 'Empresas') {
        const novaLista = this.empresasSubject.value.filter((e) => e.id !== id);
        this.empresasSubject.next(novaLista);
      } else {
        const novaLista = this.filiaisSubject.value.filter((f) => f.id !== id);
        this.filiaisSubject.next(novaLista);
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
      const empresasAtuais = this.empresasSubject.value;
      (this.newRowData as Filial).empresaId = empresasAtuais.length > 0 ? empresasAtuais[0].id : '';
    }
  }

  cancelCreate() {
    this.isCreating = false;
    this.newRowData = {};
  }

  saveCreate() {
    if (!this.newRowData.numero || !this.newRowData.nome) return;

    if (this.activeTab === 'Empresas') {
      const novaLista = [...this.empresasSubject.value, this.newRowData as Empresa];
      this.empresasSubject.next(novaLista);
    } else {
      const novaLista = [...this.filiaisSubject.value, this.newRowData as Filial];
      this.filiaisSubject.next(novaLista);
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
