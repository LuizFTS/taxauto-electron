import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { WindowLayout } from './layouts/window-layout/window-layout';
import { LivrosFiscais } from './pages/livros-fiscais/livros-fiscais';
import { Filiais } from './pages/filiais/filiais';
import { Apuracao } from './pages/apuracao/apuracao';
import { Processamento } from './pages/apuracao/components/processamento/processamento';
import { Resultado } from './pages/apuracao/components/resultado/resultado';
import { Difal } from './pages/difal/difal';

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
        path: 'difal',
        component: Difal,
      },
      {
        path: 'apuracao',
        component: Apuracao,
        children: [
          {
            path: 'processamento/:id',
            component: Processamento,
          },
          {
            path: 'resultado/:id',
            component: Resultado,
          },
        ],
      },
    ],
  },
];
