import { Component, inject, signal } from '@angular/core';
import { Card, DragAndDropArea, Button } from '../../../shared';
import { NotificationService, MergeExcelFilesService } from '../../../core';
import type { MergeExcelFilesRequest } from '../../../core/models/automation/merge-excel-files-request.model';

@Component({
  selector: 'app-merge-excel-files',
  imports: [Card, DragAndDropArea, Button],
  templateUrl: './merge-excel-files.html',
  styleUrl: './merge-excel-files.scss',
})
export class MergeExcelFiles {
  private notificationService = inject(NotificationService);
  private mergeExcelFilesService = inject(MergeExcelFilesService);
  files = signal<string[]>([]);

  isLoading = false;

  onFilesChanged(files: string[]) {
    this.files.set(files);
  }

  async executar() {
    if (this.files().length === 0) {
      this.notificationService.alert('Atenção', 'Nenhum arquivo foi selecionado.');
      return;
    }

    if (this.files().length === 1) {
      this.notificationService.alert('Atenção', 'Selecione pelo menos 2 arquivos.');
      return;
    }
    this.isLoading = true;

    const output_path = await window.electron.invoke('select-directory', null);
    if (!output_path || typeof output_path !== 'string') {
      this.notificationService.alert('Atenção', 'Nenhum diretório foi selecionado.');
      this.isLoading = false;
      return;
    }

    const payload: MergeExcelFilesRequest = {
      paths: this.files(),
      output_path: output_path,
    };

    try {
      this.mergeExcelFilesService.execute(payload).subscribe({
        next: () => {
          this.notificationService.success('Sucesso', 'Arquivos consolidados com sucesso.');
          this.isLoading = false;
        },
        error: (error) => {
          this.notificationService.error('Erro', error.message);
          this.isLoading = false;
        },
      });
    } catch {
      this.notificationService.error('Erro', 'Erro ao consolidar arquivos.');
      this.isLoading = false;
    }
  }
}
