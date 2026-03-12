export interface GrupoEmpresas {
  id: string;
  name: string;
  branches: {
    id: string;
    codigo: string;
    name: string;
  }[];
}
