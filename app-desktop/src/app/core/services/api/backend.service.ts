import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class BackendService {
  private port: number | null = null;

  async init() {
    this.port = await window.electron.getPort();
  }

  get api(): string {
    if (!this.port) {
      throw new Error('Backend não inicializado');
    }

    return `http://127.0.0.1:${this.port}/api/v1`;
  }
}
