import { Component, inject, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ModalService } from '../../../../services/modal.service';
import { ElectronService, Branch, BranchGroup } from '../../../../services/electron.service';

@Component({
  standalone: true,
  selector: 'app-filiais-modal',
  templateUrl: './filiais-modal.html',
  styleUrl: './filiais-modal.scss',
  imports: [CommonModule, FormsModule],
})
export class FiliaisModal implements OnInit {
  @Input() title: string = 'Seleção de filiais';
  @Input() subtitle: string = 'Selecione os grupos ou filiais individuais para execução';
  @Input() onConfirm?: (branches: string[]) => void;

  private modalService = inject(ModalService);
  private electronService = inject(ElectronService);

  branches: Branch[] = [];
  filteredBranches: Branch[] = [];
  groups: BranchGroup[] = [];

  selectedBranches: Set<string> = new Set<string>();
  selectedGroup: string | null = null;

  searchText: string = '';

  ngOnInit() {
    this.electronService.getBranches().subscribe((data) => {
      this.branches = data;
      this.filteredBranches = [...this.branches];
    });

    this.electronService.getGroups().subscribe((data) => {
      this.groups = data;
    });
  }

  filterBranches() {
    const text = this.searchText.toLowerCase().trim();
    if (!text) {
      this.filteredBranches = [...this.branches];
      return;
    }
    this.filteredBranches = this.branches.filter(
      (b) => b.id.includes(text) || b.uf.toLowerCase().includes(text),
    );
  }

  toggleBranch(branchId: string) {
    if (this.selectedBranches.has(branchId)) {
      this.selectedBranches.delete(branchId);
      // Unselect group if a branch is unselected
      if (this.selectedGroup) {
        const group = this.groups.find((g) => g.id === this.selectedGroup);
        if (group && group.branches.includes(branchId)) {
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
        group.branches.forEach((bId) => this.selectedBranches.add(bId));
      }
    }
  }

  selectAll() {
    this.selectedGroup = null;
    this.branches.forEach((b) => this.selectedBranches.add(b.id));
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
