import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Sidemenu } from '../../components/sidemenu/sidemenu';
import { Topbar } from '../../components/topbar/topbar';

@Component({
  selector: 'app-window-layout',
  imports: [Topbar, RouterOutlet, Sidemenu],
  templateUrl: './window-layout.html',
  styleUrl: './window-layout.scss',
})
export class WindowLayout {}
