export interface ElectronAPI {
  send: (channel: string) => void;
  invoke: (channel: string, data: unknown) => Promise<string | null>;
  getPort: () => Promise<number>;
  focusWindow: () => void;
}

declare global {
  interface Window {
    electron: ElectronAPI;
  }
}
