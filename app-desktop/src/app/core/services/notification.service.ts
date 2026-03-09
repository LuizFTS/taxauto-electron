import { Injectable, inject } from '@angular/core';
import { ModalService } from './modal.service';
import {
  NotificationModalComponent,
  NotificationModalData,
} from '../../shared/components/notification-modal/notification-modal';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private modalService = inject(ModalService);

  success(title: string, message: string, onConfirm?: () => void) {
    this.open({ type: 'success', title, message, onConfirm });
  }

  error(title: string, message: string, onConfirm?: () => void) {
    this.open({ type: 'error', title, message, onConfirm });
  }

  alert(title: string, message: string, onConfirm?: () => void) {
    this.open({ type: 'alert', title, message, onConfirm });
  }

  confirm(title: string, message: string, onConfirm: () => void, onCancel?: () => void) {
    this.open({ type: 'confirmation', title, message, onConfirm, onCancel });
  }

  private open(data: NotificationModalData) {
    this.modalService.open({
      component: NotificationModalComponent,
      data: data as Partial<NotificationModalComponent>,
      options: {
        closeOnBackdrop: data.type !== 'confirmation', // Only allow closing on backdrop if not a confirmation
      },
    });
  }
}
