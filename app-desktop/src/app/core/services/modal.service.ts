import { effect, Injectable, signal } from '@angular/core';
import { ModalConfig } from '../types/modal';

@Injectable({
  providedIn: 'root',
})
export class ModalService {
  private _modal = signal<ModalConfig<object> | null>(null);

  readonly modal = this._modal.asReadonly();

  constructor() {
    effect(() => {
      document.body.style.overflow = this._modal() ? 'hidden' : '';
    });
  }

  open<T extends object>(config: ModalConfig<T>) {
    this._modal.set(config);
  }

  confirm(result: unknown) {
    this._modal()?.onConfirm?.(result);
    this.close();
  }

  cancel() {
    this._modal()?.onCancel?.();
    this.close();
  }

  close() {
    this._modal.set(null);
  }

  isOpen() {
    return this._modal() !== null;
  }
}
