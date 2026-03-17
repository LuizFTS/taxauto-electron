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
      if (this._modal()) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    });
  }

  open<T extends object>(config: ModalConfig<T>) {
    this._modal.set(config);
  }

  close() {
    this._modal.set(null);
  }

  isOpen() {
    return this._modal() !== null;
  }
}
