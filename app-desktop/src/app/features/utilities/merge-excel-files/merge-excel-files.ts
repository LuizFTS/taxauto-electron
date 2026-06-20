import { Component, inject, signal } from '@angular/core';
import { Card, Button } from '../../../shared';
import { NotificationService, MergeExcelFilesService, LoadingService } from '../../../core';
import type { MergeExcelFilesRequest } from '../../../core/models/automation/merge-excel-files-request.model';
import { DragAndDropArea } from './components/drag-and-drop-area/drag-and-drop-area';

@Component({
  selector: 'app-merge-excel-files',
  imports: [Card, DragAndDropArea, Button],
  templateUrl: './merge-excel-files.html',
  styleUrl: './merge-excel-files.scss',
})
export class MergeExcelFiles {
  private notificationService = inject(NotificationService);
  private mergeExcelFilesService = inject(MergeExcelFilesService);
  private loadingService = inject(LoadingService);
  files = signal<string[]>([]);

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

    const output_path = await window.electron.invoke('select-directory', null);
    if (!output_path || typeof output_path !== 'string') {
      this.notificationService.alert('Atenção', 'Nenhum diretório foi selecionado.');
      this.loadingService.hide();
      return;
    }

    const payload: MergeExcelFilesRequest = {
      paths: this.files(),
      output_path: output_path,
    };

    try {
      this.loadingService.show();
      this.mergeExcelFilesService.execute(payload).subscribe({
        next: () => {
          this.notificationService.success('Sucesso', 'Arquivos consolidados com sucesso.');
          this.loadingService.hide();
        },
        error: (error) => {
          this.notificationService.error('Erro', error.message);
          this.loadingService.hide();
        },
      });
    } catch {
      this.notificationService.error('Erro', 'Erro ao consolidar arquivos.');
      this.loadingService.hide();
    }
  }

  get isLoading() {
    return this.loadingService.isLoading();
  }
}
