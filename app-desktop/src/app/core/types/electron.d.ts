import type { Observable } from 'rxjs';

export interface ElectronAPI {
  send: (channel: string) => void;
  invoke: (channel: string, data: unknown) => Observable<unknown>;
}

declare global {
  interface Window {
    electron: ElectronAPI;
  }
}
