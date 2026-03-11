import {
  Component,
  ChangeDetectionStrategy,
  CUSTOM_ELEMENTS_SCHEMA,
  inject,
  type OnInit,
  signal,
  type WritableSignal,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { Button } from '../../shared/components/button/button';
import { MatIcon } from '@angular/material/icon';
import { NotificationService, type Empresa, type Filial } from '../../core';
import { BranchService } from '../../core/services/api/data/branch.service';
import { CompanyService } from '../../core/services/api/data/company.service';
import { CompanyMapper } from '../../shared/mappers/company.mapper';
import { BehaviorSubject, combineLatest, map, switchMap, type Observable } from 'rxjs';
import { CompaniesTable } from './components/company-table/companies-table';
import { BranchTable } from './components/branch-table/branch-table';
import { BranchGroupsTable } from './components/branch-groups/branch-groups-table';
import {
  validarEFiltrarCNPJ,
  validarEFiltrarIE,
  validarEFormatarUF,
} from '../../shared/validators/validators';

@Component({
  selector: 'app-filiais',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    Button,
    MatIcon,
    FormsModule,
    CompaniesTable,
    BranchTable,
    BranchGroupsTable,
  ],
  templateUrl: './filiais.html',
  styleUrl: './filiais.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class Filiais implements OnInit {
  private branchService = inject(BranchService);
  private companyService = inject(CompanyService);
  private notificationService = inject(NotificationService);

  activeTab: 'Empresas' | 'Filiais' | 'Grupos' = 'Filiais';

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
  newRowData: WritableSignal<Partial<Empresa | Filial>> = signal<Partial<Empresa | Filial>>({});

  get editingFilialData() {
    return this.editingRows as Record<string, Partial<Filial>>;
  }

  get editingEmpresaData() {
    return this.editingRows as Record<string, Partial<Empresa>>;
  }

  get newFilialData() {
    return this.newRowData() as Partial<Filial>;
  }
  get newEmpresaData() {
    return this.newRowData() as Partial<Empresa>;
  }

  ngOnInit() {
    this.refreshData();
  }

  private refreshData() {
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

  setActiveTab(tab: 'Empresas' | 'Filiais' | 'Grupos') {
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
    if (this.activeTab === 'Empresas') {
      const editEmpresaData = this.editingEmpresaData[id];
      if (!editEmpresaData?.nome) {
        this.notificationService.alert('Alerta', 'Nome é obrigatório');
        return;
      }
      const status = editEmpresaData.status === 'Ativo';
      this.updateCompany(parseInt(id), editEmpresaData.nome!, status);
      delete this.editingEmpresaData[id];
    } else {
      const editFilialData = this.editingFilialData[id];
      // --- VALIDAÇÕES E TRATAMENTOS ---
      const ufValida = validarEFormatarUF(editFilialData.uf || '');
      const cnpjValido = validarEFiltrarCNPJ(editFilialData.cnpj || '');
      const ieValido = validarEFiltrarIE(editFilialData.ie || '');
      const nomeValido = editFilialData.nome?.toUpperCase().trim();

      if (!nomeValido || nomeValido.length < 3) {
        this.notificationService.alert(
          'Alerta',
          'Nome inválido, Por favor, informe um nome válido.',
        );
        return;
      }

      if (!ufValida) {
        this.notificationService.alert(
          'Alerta',
          'UF inválida! Por favor, informe uma UF válida (ex: SP, RJ).',
        );
        return;
      }

      if (!cnpjValido) {
        this.notificationService.alert(
          'Alerta',
          'CNPJ inválido! O CNPJ deve conter 14 dígitos numéricos.',
        );
        return;
      }
      if (!ieValido) {
        this.notificationService.alert(
          'Alerta',
          'IE inválida! A IE deve conter no mínimo 5 dígitos numéricos.',
        );
        return;
      }

      const status = editFilialData.status === 'Ativo';

      this.updateBranch(
        parseInt(id),
        nomeValido,
        ufValida,
        cnpjValido,
        ieValido,
        parseInt(editFilialData.empresaId!),
        status,
      );

      delete this.editingFilialData[id];
    }
  }

  deleteRow(id: string) {
    this.notificationService.confirm(
      'Confirmação',
      'Tem certeza que deseja excluir registro?',
      () => {
        if (this.activeTab === 'Empresas') {
          this.deleteCompany(id);
        } else {
          this.deleteBranch(id);
        }
      },
    );
  }

  // --- Create ---
  startCreate() {
    if (this.activeTab === 'Empresas') {
      this.newEmpresaData.numero = '';
      this.newEmpresaData.nome = '';
      this.newEmpresaData.status = 'Ativo';
    } else {
      this.newFilialData.numero = '';
      this.newFilialData.nome = '';
      this.newFilialData.uf = '';
      this.newFilialData.cnpj = '';
      this.newFilialData.ie = '';
      this.newFilialData.status = 'Ativo';
    }
    this.isCreating = true;

    if (this.activeTab === 'Filiais') {
      const empresasAtuais = this.empresasSubject.value;
      this.newFilialData.empresaId = empresasAtuais.length > 0 ? empresasAtuais[0].id : '';
    }
  }

  cancelCreate() {
    this.isCreating = false;
    this.newRowData.set({});
  }

  saveCreate() {
    if (this.activeTab === 'Empresas') {
      const empresaData = this.newEmpresaData;
      // Validação simples para Empresa
      if (!empresaData.nome || empresaData.nome.trim().length < 3) {
        this.notificationService.alert(
          'Alerta',
          'O nome da empresa deve ter pelo menos 3 caracteres.',
        );
        return;
      }

      this.createCompany();
    } else {
      // --- VALIDAÇÕES PARA FILIAL ---
      const filialData = this.newFilialData; // Cast para ajudar o TS

      const ufValida = validarEFormatarUF(filialData.uf || '');
      const cnpjValido = validarEFiltrarCNPJ(filialData.cnpj || '');
      const ieValida = validarEFiltrarIE(filialData.ie || '');
      const nomeValido = filialData.nome?.toUpperCase().trim();

      if (!nomeValido || nomeValido.length < 3) {
        console.log(!nomeValido);

        console.log(filialData);

        this.notificationService.alert('Alerta', 'O nome da filial é obrigatório.');
        return;
      }

      if (!ufValida) {
        this.notificationService.alert('Alerta', 'UF inválida! Use siglas como SP, RJ, etc.');
        return;
      }

      if (!cnpjValido) {
        this.notificationService.alert('Alerta', 'CNPJ inválido! Deve conter 14 números.');
        return;
      }

      if (!ieValida) {
        this.notificationService.alert(
          'Alerta',
          'IE inválida! A IE deve conter no mínimo 5 dígitos numéricos.',
        );
        return;
      }

      if (!filialData.empresaId) {
        this.notificationService.alert(
          'Alerta',
          'É necessário selecionar uma Empresa para esta filial.',
        );
        return;
      }
      this.newRowData.update((current) => ({
        ...current,
        nome: nomeValido,
        uf: ufValida,
        cnpj: cnpjValido,
        ie: ieValida,
      }));

      this.createBranch();
    }

    this.isCreating = false;
    this.newRowData.set({});
  }

  updateEditField(id: string, field: string, event: Event) {
    const target = event.target as HTMLInputElement | HTMLSelectElement;
    const row = this.editingRows[id] as Record<string, unknown>;
    row[field] = target.value;
  }

  updateCreateField(field: string, event: Event) {
    const target = event.target as HTMLInputElement | HTMLSelectElement;
    const value = target.value;

    this.newRowData.update((current) => ({
      ...current,
      [field as keyof (Filial | Empresa)]: value,
    }));
  }

  // API calls
  private deleteBranch(id: string) {
    if (Number.isNaN(Number(id))) {
      return;
    }

    try {
      this.branchService.deleteBranch(parseInt(id)).subscribe(() => {
        this.refreshData();
      });
    } catch (error) {
      console.error(error);
      this.notificationService.error('Erro', 'Erro ao excluir registro');
    }
  }

  private deleteCompany(id: string) {
    if (Number.isNaN(Number(id))) {
      return;
    }
    try {
      this.companyService.deleteCompany(parseInt(id)).subscribe(() => {
        this.refreshData();
      });
    } catch (error) {
      console.error(error);
      this.notificationService.error('Erro', 'Erro ao excluir registro');
    }
  }

  private createBranch() {
    try {
      this.branchService
        .createBranch({
          codigo: this.newFilialData.numero!,
          nome: this.newFilialData.nome!,
          uf: this.newFilialData.uf!,
          cnpj: this.newFilialData.cnpj!,
          ie: this.newFilialData.ie!,
          company_id: parseInt(this.newFilialData.empresaId!),
        })
        .subscribe(() => {
          this.refreshData();
        });
    } catch (error) {
      console.error(error);
      this.notificationService.error('Erro', 'Erro ao criar filial');
    }
  }

  private createCompany() {
    try {
      console.log(this.newEmpresaData);
      this.companyService
        .createCompany({
          codigo: this.newEmpresaData.numero!,
          nome: this.newEmpresaData.nome!,
        })
        .subscribe(() => {
          this.refreshData();
        });
    } catch (error) {
      console.error(error);
      this.notificationService.error('Erro', 'Erro ao criar empresa');
    }
  }

  private updateBranch(
    id: number,
    name: string,
    uf: string,
    cnpj: string,
    ie: string,
    company_id: number,
    status: boolean,
  ) {
    console.log('test');
    try {
      this.branchService
        .updateBranch(id, {
          name,
          uf,
          cnpj,
          ie,
          company_id,
          status,
        })
        .subscribe(() => {
          this.refreshData();
        });
    } catch (error) {
      console.error(error);
      this.notificationService.error('Erro', 'Erro ao salvar informações atualizadas.');
    }
  }

  private updateCompany(id: number, name: string, status: boolean) {
    try {
      this.companyService.updateCompany(id, name, status).subscribe(() => {
        this.refreshData();
      });
    } catch (error) {
      console.error(error);
      this.notificationService.error('Erro', 'Erro ao salvar informações atualizadas.');
    }
  }
}
