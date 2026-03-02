import type { Type } from '@angular/core';

export interface ModalConfig<T extends Object> {
  component: Type<T>;
  data?: Partial<T>;
  options?: {
    closeOnBackdrop?: boolean;
  };
}
