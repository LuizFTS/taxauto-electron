import { Component, inject, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  ModalService,
  ElectronService,
  BranchService,
  type GrupoEmpresas,
  type Filial,
  CompanyService,
} from '../../../../core';
import { BehaviorSubject, combineLatest, map, switchMap, type Observable } from 'rxjs';
import { CompanyMapper } from '../../../../shared/mappers/company.mapper';

@Component({
  standalone: true,
  selector: 'app-filiais-modal',
  templateUrl: './filiais-modal.html',
  styleUrl: './filiais-modal.scss',
  imports: [CommonModule, FormsModule],
})
export class FiliaisModal implements OnInit {
  @Input() title = 'Seleção de filiais';
  @Input() subtitle = 'Selecione os grupos ou filiais individuais para execução';
  @Input() onConfirm?: (branches: string[]) => void;

  private modalService = inject(ModalService);
  private electronService = inject(ElectronService);
  private branchService = inject(BranchService);
  private companyService = inject(CompanyService);

  private filiaisSubject = new BehaviorSubject<Filial[]>([]);

  branches$!: Observable<Filial[]>;
  groups: GrupoEmpresas[] = [];

  selectedBranches: Set<string> = new Set<string>();
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
      });
    this.branches$ = combineLatest([this.filiaisSubject, this.searchSubject]).pipe(
      map(([list, q]) =>
        list.filter((f) => {
          const branchNumber = parseInt(f.numero, 10);
          const searchNumber = parseInt(q, 10);
          const numberMatch = !isNaN(searchNumber) && branchNumber === searchNumber;
          const ufMatch = f.uf.toLowerCase().includes(q.toLowerCase());

          return numberMatch || ufMatch;
        }),
      ),
    );

    this.electronService.getGroups().subscribe((data) => {
      this.groups = data;
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
        group.branches.forEach((bId) => this.selectedBranches.add(bId.id));
      }
    }
  }

  selectAll() {
    this.selectedGroup = null;

    const currentBranches = this.filiaisSubject.value;

    currentBranches.forEach((b) => this.selectedBranches.add(b.numero));
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
}
