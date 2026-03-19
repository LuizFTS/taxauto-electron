import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidemenu',
  imports: [RouterLink, RouterLinkActive, MatIconModule],
  templateUrl: './sidemenu.html',
  styleUrl: './sidemenu.scss',
})
export class Sidemenu {
  isOpen = false;

  menuItems = [
    {
      title: 'Automação',
      items: [
        {
          title: 'Livros fiscais',
          icon: 'book',
          route: '/livros-fiscais',
        },
        /* {
          title: 'Notas canceladas',
          icon: 'cancel',
          route: '/notas-canceladas',
        },
        {
          title: 'Congelar periodos',
          icon: 'lock',
          route: '/congelar-periodos',
        }, */
      ],
    },
    /* {
      title: 'Utilitários',
      items: [
        {
          title: 'Consolidar Excel',
          icon: 'handyman',
          route: '/consolidar-excel',
        },
      ],
    }, */
  ];

  toggleMenu(): void {
    this.isOpen = !this.isOpen;
  }
}
