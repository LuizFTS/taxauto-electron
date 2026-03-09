import { Component, Input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { Button } from '../button/button';
import { ModalService } from '../../../core/services/modal.service';

export type NotificationType = 'success' | 'error' | 'alert' | 'confirmation';

export interface NotificationModalData {
  type: NotificationType;
  title: string;
  message: string;
  onConfirm?: () => void;
  onCancel?: () => void;
  confirmText?: string;
  cancelText?: string;
}

@Component({
  selector: 'app-notification-modal',
  standalone: true,
  imports: [CommonModule, MatIconModule, Button],
  templateUrl: './notification-modal.html',
  styleUrl: './notification-modal.scss',
})
export class NotificationModalComponent {
  private modalService = inject(ModalService);

  @Input() type: NotificationType = 'alert';
  @Input() title = '';
  @Input() message = '';
  @Input() confirmText = 'OK';
  @Input() cancelText = 'Cancelar';
  @Input() onConfirm?: () => void;
  @Input() onCancel?: () => void;

  get icon(): string {
    switch (this.type) {
      case 'success':
        return 'check_circle';
      case 'error':
        return 'error';
      case 'alert':
        return 'warning';
      case 'confirmation':
        return 'help_outline';
      default:
        return 'info';
    }
  }

  get iconClass(): string {
    return `icon-${this.type}`;
  }

  handleConfirm() {
    if (this.onConfirm) {
      this.onConfirm();
    }
    this.modalService.close();
  }

  handleCancel() {
    if (this.onCancel) {
      this.onCancel();
    }
    this.modalService.close();
  }
}
