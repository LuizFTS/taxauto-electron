import { effect, Injectable, signal } from '@angular/core';
import { ModalConfig } from '../types/modal.types';

@Injectable({
  providedIn: 'root',
})
export class ModalService {
  private _modal = signal<ModalConfig<Object> | null>(null);

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

  open<T extends Object>(config: ModalConfig<T>) {
    console.log(config);
    this._modal.set(config);
  }

  close() {
    this._modal.set(null);
  }

  isOpen() {
    return this._modal() !== null;
  }
}
