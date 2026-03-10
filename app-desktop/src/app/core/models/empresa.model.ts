import type { Filial } from './filial.model';

export interface Empresa {
  id: string;
  numero: string;
  nome: string;
  filiais: Filial[];
  status: 'Ativo' | 'Inativo';
}
