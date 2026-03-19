import { Component, CUSTOM_ELEMENTS_SCHEMA, ViewEncapsulation } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-topbar',
  imports: [MatIconModule],
  templateUrl: './topbar.html',
  styleUrl: './topbar.scss',
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  encapsulation: ViewEncapsulation.None,
})
export class Topbar {
  private electron = window.electron;

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
