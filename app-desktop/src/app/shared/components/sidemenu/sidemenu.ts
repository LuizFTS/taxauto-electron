import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidemenu',
  imports: [RouterLink, RouterLinkActive, MatIconModule],
  templateUrl: './sidemenu.html',
  styleUrl: './sidemenu.scss',
})
export class Sidemenu {}
