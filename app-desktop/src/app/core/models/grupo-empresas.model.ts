import type { Filial } from './filial.model';

export interface GrupoEmpresas {
  id: string;
  name: string;
  branches: Filial[];
}
