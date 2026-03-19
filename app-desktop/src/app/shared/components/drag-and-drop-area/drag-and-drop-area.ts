import { Component, EventEmitter, Output, NO_ERRORS_SCHEMA, inject, Input } from '@angular/core';
import { NotificationService } from '../../../core/services/notification.service';

@Component({
  selector: 'app-drag-and-drop-area',
  imports: [],
  templateUrl: './drag-and-drop-area.html',
  styleUrl: './drag-and-drop-area.scss',
  schemas: [NO_ERRORS_SCHEMA],
})
export class DragAndDropArea {
  private notificationService = inject(NotificationService);
  @Output() filesChanged = new EventEmitter<string[]>();

  // method received by parent component to clean all files
  @Input() cleanFiles = () => {
    this.files = [];
    this.filesChanged.emit(this.files);
  };

  isDragOver = false;
  files: string[] = [];

  draggedItemIndex: number | null = null;
  dragOverItemIndex: number | null = null;

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;

    if (event.dataTransfer?.files) {
      const droppedFiles = Array.from(event.dataTransfer.files);

      const validFiles = droppedFiles
        .filter((f) => f.name.endsWith('.csv') || f.name.endsWith('.xlsx'))
        .map((f) => window.electron.getFilePath(f));

      if (validFiles.length > 0) {
        this.addFiles(validFiles);
      }
    }
  }

  async openFileSelector() {
    if (window.electron) {
      const selectedFiles = await window.electron.invoke('select-files', null);
      if (Array.isArray(selectedFiles) && selectedFiles.length > 0) {
        this.addFiles(selectedFiles);
      }
    }
  }

  addFiles(newFiles: string[]) {
    // if file already is on the list, do not add it again and call notificationservice with an alert to the user
    const alreadyFiles = newFiles.filter((file) => this.files.includes(file));
    // get filename from path
    const alreadyFilesNames = alreadyFiles.map((file) => this.getFileName(file));

    if (alreadyFiles.length > 0) {
      this.notificationService.alert(
        'Atenção',
        `${alreadyFilesNames.length > 1 ? 'Os arquivos' : 'O arquivo'} ${alreadyFilesNames.join(', ')} ${alreadyFiles.length > 1 ? 'já constam' : 'já consta'} na seleção de arquivos.`,
      );
    }

    const currentSet = new Set(this.files);
    newFiles.forEach((file) => currentSet.add(file));
    this.files = Array.from(currentSet);
    this.filesChanged.emit(this.files);
  }

  removeFile(index: number) {
    this.files.splice(index, 1);
    this.filesChanged.emit(this.files);
  }

  onItemDragStart(index: number) {
    this.draggedItemIndex = index;
  }

  onItemDragOver(event: DragEvent, index: number) {
    event.preventDefault();
    if (this.draggedItemIndex !== null && this.draggedItemIndex !== index) {
      this.dragOverItemIndex = index;
    }
  }

  onItemDragLeave() {
    this.dragOverItemIndex = null;
  }

  onItemDrop(event: DragEvent, index: number) {
    event.preventDefault();
    event.stopPropagation();

    if (this.draggedItemIndex !== null && this.draggedItemIndex !== index) {
      const draggedFile = this.files[this.draggedItemIndex];
      this.files.splice(this.draggedItemIndex, 1);
      this.files.splice(index, 0, draggedFile);
      this.filesChanged.emit(this.files);
    }

    this.draggedItemIndex = null;
    this.dragOverItemIndex = null;
  }

  onItemDragEnd() {
    this.draggedItemIndex = null;
    this.dragOverItemIndex = null;
  }

  getFileName(filePath: string): string {
    return filePath.split(/[/\\]/).pop() || filePath;
  }
}
