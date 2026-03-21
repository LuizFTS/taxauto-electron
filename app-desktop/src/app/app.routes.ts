import { Routes } from '@angular/router';
import { WindowLayout } from './shared';
import { LivrosFiscais } from './features/taxauto/livros-fiscais/livros-fiscais';
import { Filiais } from './features/filiais/filiais';
import { Apuracao } from './features/taxdata/apuracao/apuracao';
import { Processamento } from './features/taxdata/apuracao/components/processamento/processamento';
import { Resultado } from './features/taxdata/apuracao/components/resultado/resultado';
import { Difal } from './features/taxdata/difal/difal';
import { MergeExcelFiles } from './features/utilities/merge-excel-files/merge-excel-files';
import { CancelledInvoices } from './features/taxauto/cancelled-invoices/cancelled-invoices';

export const routes: Routes = [
  {
    path: '',
    component: WindowLayout,
    children: [
      {
        path: 'taxauto',
        children: [
          {
            path: 'livros-fiscais',
            component: LivrosFiscais,
          },
          {
            path: 'cancelled-invoices',
            component: CancelledInvoices,
          },
        ],
      },
      {
        path: 'taxdata',
        children: [
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
      {
        path: 'utilitarios',
        children: [
          {
            path: 'merge-excel-files',
            component: MergeExcelFiles,
          },
          {
            path: 'branch-manager',
            component: Filiais,
          },
        ],
      },
    ],
  },
];
