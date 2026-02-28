import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-topbar',
  imports: [MatIconModule],
  templateUrl: './topbar.html',
  styleUrl: './topbar.scss',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class Topbar {
  private electron = (window as any).electron;

  minimizeWindow() {
    this.electron?.send('window-minimize');
  }

  maximizeWindow() {
    this.electron?.send('window-maximize');
  }

  closeWindow() {
    this.electron?.send('window-close');
  }
}
