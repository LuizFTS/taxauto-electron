import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { WindowLayout } from './layouts/window-layout/window-layout';
import { LivrosFiscais } from './pages/livros-fiscais/livros-fiscais';
import { Filiais } from './pages/filiais/filiais';
import { Apuracao } from './pages/apuracao/apuracao';

export const routes: Routes = [
  {
    path: '',
    component: WindowLayout,
    children: [
      {
        path: 'home',
        component: Home,
      },
      {
        path: 'livros-fiscais',
        component: LivrosFiscais,
      },
      {
        path: 'filiais',
        component: Filiais,
      },
      {
        path: 'apuracao',
        component: Apuracao,
      },
    ],
  },
];
