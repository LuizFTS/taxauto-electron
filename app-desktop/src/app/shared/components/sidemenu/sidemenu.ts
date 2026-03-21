import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidemenu',
  imports: [RouterLink, RouterLinkActive, MatIconModule],
  templateUrl: './sidemenu.html',
  styleUrl: './sidemenu.scss',
})
export class Sidemenu {
  @Input() isOpen = false;
  @Output() toggleSideMenu = new EventEmitter<void>();

  menuItems = [
    {
      title: 'Automação',
      items: [
        {
          title: 'Gerar Relatórios',
          icon: 'book',
          route: '/taxauto/livros-fiscais',
        },
        /* {
          title: 'Notas canceladas',
          icon: 'cancel',
          route: '/taxauto/cancelled-invoices',
        },
        {
          title: 'Congelar periodos',
          icon: 'lock',
          route: '/taxauto/congelar-periodos',
        }, */
      ],
    },
    {
      title: 'TaxTrack',
      items: [
        {
          title: 'Dashboard',
          icon: 'dashboard',
          route: '/taxtrack/dashboard',
        },
      ],
    },
    {
      title: 'Utilitários',
      items: [
        {
          title: 'Consolidar Excel',
          icon: 'handyman',
          route: '/utilitarios/merge-excel-files',
        },
        {
          title: 'Gerenciar filiais',
          icon: 'domain',
          route: '/utilitarios/branch-manager',
        },
      ],
    },
  ];

  toggleMenu(): void {
    this.toggleSideMenu.emit();
  }
}
