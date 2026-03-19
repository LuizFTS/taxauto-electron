export interface ElectronAPI {
  send: (channel: string) => void;
  invoke: (channel: string, data: unknown) => Promise<string[] | string | null>;
  getPort: () => Promise<number>;
  focusWindow: () => void;
  getFilePath: (file: File) => string;
}

declare global {
  interface Window {
    electron: ElectronAPI;
  }
}
