import { Component, ChangeDetectionStrategy, ChangeDetectorRef, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Sidemenu } from '../../components/sidemenu/sidemenu';
import { Topbar } from '../../components/topbar/topbar';

@Component({
  selector: 'app-window-layout',
  imports: [Topbar, RouterOutlet, Sidemenu],
  templateUrl: './window-layout.html',
  styleUrl: './window-layout.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class WindowLayout {
  sideMenuOpen = false;
  cdr: ChangeDetectorRef = inject(ChangeDetectorRef);

  toggleSideMenu(): void {
    this.sideMenuOpen = !this.sideMenuOpen;
    console.log(this.sideMenuOpen);
    this.cdr.detectChanges();
  }

  get sideMenuOpenClass(): string {
    return this.sideMenuOpen ? 'side-menu-open' : '';
  }
}
