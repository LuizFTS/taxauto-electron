import { Component, EventEmitter, Output, Input, NO_ERRORS_SCHEMA } from '@angular/core';

@Component({
  selector: 'app-drag-and-drop',
  imports: [],
  templateUrl: './drag-and-drop.html',
  styleUrl: './drag-and-drop.scss',
  schemas: [NO_ERRORS_SCHEMA],
})
export class DragAndDrop {
  @Input() selectedFile: { name: string; sizeStr: string; statusText: string } | null = null;

  @Output() filesChanged = new EventEmitter<{ files: string[] }>();
  @Output() fileRemoved = new EventEmitter<void>();

  isDragOver = false;

  onDragOver(event: DragEvent) {
    if (this.selectedFile) return;
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = true;
  }

  onDragLeave(event: DragEvent) {
    if (this.selectedFile) return;
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragOver = false;

    if (this.selectedFile) return;

    if (event.dataTransfer?.files) {
      const droppedFiles = Array.from(event.dataTransfer.files);

      const validFiles = droppedFiles
        .filter(
          (f) =>
            f.name.endsWith('.csv') ||
            f.name.endsWith('.xlsx') ||
            f.name.endsWith('.xlsm') ||
            f.name.endsWith('.xls'),
        )
        .map((f) => window.electron.getFilePath(f));

      if (validFiles.length > 0) {
        this.addFiles(validFiles);
      }
    }
  }

  async openFileSelector() {
    if (this.selectedFile) return;

    if (window.electron) {
      const selectedFiles = await window.electron.invoke('select-files', null);
      if (Array.isArray(selectedFiles) && selectedFiles.length > 0) {
        this.addFiles(selectedFiles);
      }
    }
  }

  addFiles(newFiles: string[]) {
    this.filesChanged.emit({ files: newFiles });
  }

  onRemoveFile(event: Event) {
    event.preventDefault();
    event.stopPropagation();
    this.fileRemoved.emit();
  }
}
