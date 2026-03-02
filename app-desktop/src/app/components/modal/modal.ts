import {
  Component,
  AfterViewInit,
  inject,
  ViewChild,
  ViewContainerRef,
  effect,
} from '@angular/core';
import { ModalService } from '../../services/modal.service';
import { MatIconModule } from '@angular/material/icon';
import { NgComponentOutlet } from '@angular/common';

@Component({
  selector: 'app-modal',
  imports: [MatIconModule, NgComponentOutlet],
  templateUrl: './modal.html',
  styleUrl: './modal.scss',
})
export class Modal {
  private modalService = inject(ModalService);

  modal = this.modalService.modal;

  close() {
    this.modalService.close();
  }

  backdropClick(closeOnBackdrop?: boolean) {
    if (closeOnBackdrop !== false) {
      this.close();
    }
  }
}
