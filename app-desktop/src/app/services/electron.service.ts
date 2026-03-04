import { Injectable } from '@angular/core';
import { from, of, type Observable } from 'rxjs';

export interface Branch {
  id: string;
  name: string;
  uf: string;
}

export interface BranchGroup {
  id: string;
  name: string;
  branches: string[];
}

@Injectable({
  providedIn: 'root',
})
export class ElectronService {
  getBranches(): Observable<Branch[]> {
    return of([
      {
        id: '1',
        name: 'Filial 1',
        uf: 'SP',
      },
      {
        id: '2',
        name: 'Filial 2',
        uf: 'RJ',
      },
      {
        id: '3',
        name: 'Filial 3',
        uf: 'MG',
      },
      {
        id: '4',
        name: 'Filial 4',
        uf: 'SP',
      },
      {
        id: '5',
        name: 'Filial 5',
        uf: 'RJ',
      },
      {
        id: '6',
        name: 'Filial 6',
        uf: 'MG',
      },
      {
        id: '7',
        name: 'Filial 7',
        uf: 'SP',
      },
      {
        id: '8',
        name: 'Filial 8',
        uf: 'RJ',
      },
      {
        id: '9',
        name: 'Filial 9',
        uf: 'MG',
      },
      {
        id: '10',
        name: 'Filial 10',
        uf: 'SP',
      },
      {
        id: '11',
        name: 'Filial 2',
        uf: 'RJ',
      },
      {
        id: '12',
        name: 'Filial 3',
        uf: 'MG',
      },
    ]);
  }

  getGroups(): Observable<BranchGroup[]> {
    return of([
      {
        id: '1',
        name: 'Grupo A',
        branches: ['1', '2'],
      },
      {
        id: '2',
        name: 'Grupo B',
        branches: ['3'],
      },
      {
        id: '3',
        name: 'Grupo C',
        branches: ['3'],
      },
      {
        id: '4',
        name: 'Grupo D',
        branches: ['3'],
      },
    ]);
  }

  executeLivrosFiscais(payload: any): Observable<any> {
    return from((window as any).electron.invoke('execute-livros-fiscais', payload));
  }
}
