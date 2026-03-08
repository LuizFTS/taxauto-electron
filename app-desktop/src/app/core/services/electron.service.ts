import { Injectable } from '@angular/core';
import { from, of, type Observable } from 'rxjs';
import type { Filial } from '../models/filial.model';
import type { GrupoEmpresas } from '../models/grupo-empresas.model';

@Injectable({
  providedIn: 'root',
})
export class ElectronService {
  getBranches(): Observable<Filial[]> {
    return of([
      {
        id: '1',
        numero: '1',
        nome: 'Filial 1',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '2',
        numero: '2',
        nome: 'Filial 2',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '3',
        numero: '3',
        nome: 'Filial 3',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '4',
        numero: '4',
        nome: 'Filial 4',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '5',
        numero: '5',
        nome: 'Filial 5',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '6',
        numero: '6',
        nome: 'Filial 6',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '7',
        numero: '7',
        nome: 'Filial 7',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '8',
        numero: '8',
        nome: 'Filial 8',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '9',
        numero: '9',
        nome: 'Filial 9',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '10',
        numero: '10',
        nome: 'Filial 10',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '11',
        numero: '11',
        nome: 'Filial 11',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '12',
        numero: '12',
        nome: 'Filial 12',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
      {
        id: '13',
        numero: '13',
        nome: 'Filial 13',
        uf: 'SP',
        empresaId: '01',
        status: 'Ativo',
      },
    ]);
  }

  getGroups(): Observable<GrupoEmpresas[]> {
    return of([
      {
        id: '1',
        name: 'Grupo A',
        branches: [
          {
            id: '1',
            numero: '1',
            nome: 'Filial 1',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '2',
            numero: '2',
            nome: 'Filial 2',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '3',
            numero: '3',
            nome: 'Filial 3',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
        ],
      },
      {
        id: '2',
        name: 'Grupo B',
        branches: [
          {
            id: '9',
            numero: '9',
            nome: 'Filial 9',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '10',
            numero: '10',
            nome: 'Filial 10',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '11',
            numero: '11',
            nome: 'Filial 11',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '12',
            numero: '12',
            nome: 'Filial 12',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '13',
            numero: '13',
            nome: 'Filial 13',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
        ],
      },
      {
        id: '3',
        name: 'Grupo C',
        branches: [
          {
            id: '6',
            numero: '6',
            nome: 'Filial 6',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '7',
            numero: '7',
            nome: 'Filial 7',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '8',
            numero: '8',
            nome: 'Filial 8',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
        ],
      },
      {
        id: '4',
        name: 'Grupo D',
        branches: [
          {
            id: '3',
            numero: '3',
            nome: 'Filial 3',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
          {
            id: '4',
            numero: '4',
            nome: 'Filial 4',
            uf: 'SP',
            empresaId: '01',
            status: 'Ativo',
          },
        ],
      },
    ]);
  }

  executeLivrosFiscais(payload: any): Observable<any> {
    return from((window as any).electron.invoke('execute-livros-fiscais', payload));
  }
}
