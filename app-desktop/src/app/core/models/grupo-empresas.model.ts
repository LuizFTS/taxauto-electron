export interface GrupoEmpresas {
  id: string;
  name: string;
  analyst: string;
  branches: {
    id: string;
    codigo: string;
    name: string;
  }[];
}
