import { Routes } from '@angular/router';
import { WindowLayout } from './shared';
import { LivrosFiscais } from './features/livros-fiscais/livros-fiscais';
import { Filiais } from './features/filiais/filiais';
import { Apuracao } from './features/apuracao/apuracao';
import { Processamento } from './features/apuracao/components/processamento/processamento';
import { Resultado } from './features/apuracao/components/resultado/resultado';
import { Difal } from './features/difal/difal';

export const routes: Routes = [
  {
    path: '',
    component: WindowLayout,
    children: [
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
