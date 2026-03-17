import { Component, computed, inject, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  ModalService,
  BranchService,
  type GrupoEmpresas,
  type Filial,
  CompanyService,
  type Empresa,
} from '../../../../core';
import { BehaviorSubject, combineLatest, map, Observable, switchMap } from 'rxjs';
import { CompanyMapper } from '../../../../shared/mappers/company.mapper';
import { BranchGroupService } from '../../../../core/services/api/data/branch-group.service';
import { GroupBranchMapper } from '../../../../shared/mappers/group-branch.mapper';
import { Select } from '../../../../shared';

@Component({
  standalone: true,
  selector: 'app-filiais-modal',
  templateUrl: './filiais-modal.html',
  styleUrl: './filiais-modal.scss',
  imports: [CommonModule, FormsModule, Select],
})
export class FiliaisModal implements OnInit {
  @Input() title = 'Seleção de filiais';
  @Input() subtitle = 'Selecione os grupos ou filiais individuais para execução';
  @Input() onConfirm?: (branches: string[]) => void;

  tiposLivro$!: Observable<{ value: number | null; label: string }[]>;

  private modalService = inject(ModalService);
  private branchService = inject(BranchService);
  private companyService = inject(CompanyService);
  private groupService = inject(BranchGroupService);

  private companyFilterSubject = new BehaviorSubject<number | null>(null);
  private filiaisSubject = new BehaviorSubject<Filial[]>([]);
  private empresasSubject = new BehaviorSubject<Empresa[]>([]);
  private readonly filiaisFiltered = computed(() => {
    const list = this.filiaisSubject.value;
    const q = this.searchSubject.value;
    return list.filter((f) => {
      const branchNumber = parseInt(f.numero, 10);
      const numberMatch = !isNaN(branchNumber) && branchNumber.toString().includes(q);
      const ufMatch = f.uf.toLowerCase().includes(q.toLowerCase());

      return numberMatch || ufMatch;
    });
  });

  branches$!: Observable<Filial[]>;
  empresas$!: Observable<Empresa[]>;
  groups: GrupoEmpresas[] = [];

  selectedBranches: Set<string> = new Set<string>();
  selectedCompany = '';
  selectedGroup: string | null = null;

  private searchSubject = new BehaviorSubject<string>('');
  searchQuery = '';

  onSearchChange(valor: string) {
    this.searchSubject.next(valor);
  }

  ngOnInit() {
    this.companyService
      .getAll()
      .pipe(
        switchMap((companies) =>
          this.branchService.getAll().pipe(map((branches) => ({ companies, branches }))),
        ),
      )
      .subscribe(({ companies, branches }) => {
        // Alimentamos os Subjects com os dados iniciais do Mapper
        this.filiaisSubject.next(CompanyMapper.toFilialList(branches, companies));
        this.empresasSubject.next(CompanyMapper.toEmpresaList(companies, branches));
      });
    this.branches$ = combineLatest([
      this.filiaisSubject,
      this.searchSubject,
      this.companyFilterSubject,
    ]).pipe(
      map(([list, q, selectedId]) => {
        return list
          .filter((f) => {
            const branchNumber = parseInt(f.numero, 10);
            const numberMatch = !isNaN(branchNumber) && branchNumber.toString().includes(q);
            const ufMatch = f.uf.toLowerCase().includes(q.toLowerCase());
            return numberMatch || ufMatch;
          })
          .filter((f) => {
            if (selectedId === null || selectedId === undefined) {
              return true;
            }
            return parseInt(f.empresaId) === selectedId;
          });
      }),
    );

    this.empresas$ = this.empresasSubject.asObservable();

    this.tiposLivro$ = this.empresas$.pipe(
      map((empresas) => {
        const listaMapeada = empresas.map((empresas) => ({
          value: parseInt(empresas.id),
          label: empresas.nome,
        }));

        return [{ value: null, label: 'Todas as empresas' }, ...listaMapeada];
      }),
    );

    this.groupService.getAll().subscribe((data) => {
      this.groups = GroupBranchMapper.toGroupBranchList(data);
    });
  }

  toggleBranch(branchId: string) {
    if (this.selectedBranches.has(branchId)) {
      this.selectedBranches.delete(branchId);
      // Unselect group if a branch is unselected
      if (this.selectedGroup) {
        const group = this.groups.find((g) => g.id === this.selectedGroup);

        if (group && group.branches.some((filial) => filial.id === branchId)) {
          this.selectedGroup = null;
        }
      }
    } else {
      this.selectedBranches.add(branchId);
    }
  }

  toggleGroup(groupId: string) {
    if (this.selectedGroup === groupId) {
      this.selectedGroup = null;
      this.clearSelection();
    } else {
      this.selectedGroup = groupId;
      const group = this.groups.find((g) => g.id === groupId);
      if (group) {
        this.selectedBranches.clear();
        group.branches.forEach((bId) => this.selectedBranches.add(bId.codigo.padStart(3, '0')));
      }
    }
  }

  selectAll() {
    this.selectedGroup = null;

    const visibleBranches = this.filiaisFiltered();

    if (visibleBranches) {
      visibleBranches.forEach((b) => {
        if (b.numero) {
          this.selectedBranches.add(b.numero);
        }
      });
    }
  }

  clearSelection() {
    this.selectedGroup = null;
    this.selectedBranches.clear();
  }

  confirm() {
    if (this.onConfirm) {
      this.onConfirm(Array.from(this.selectedBranches));
    }
    this.modalService.close();
  }

  cancel() {
    this.modalService.close();
  }

  onCompanySelect(event: { value: number | null; label: string }) {
    this.selectedCompany = event.value?.toString() || '';
    this.selectedBranches.clear();
    this.selectedGroup = null;
    this.companyFilterSubject.next(event.value);
  }

  formatGroupName(value: string) {
    const firstWord = value.split(' ')[0];
    const remainingWords = value.split(' ').slice(1).join(' ');

    return (
      firstWord.charAt(0).toUpperCase() +
      firstWord.slice(1).toLowerCase() +
      ' ' +
      remainingWords.toUpperCase()
    );
  }
}
