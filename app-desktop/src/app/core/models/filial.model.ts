export interface Filial {
  id: string;
  numero: string;
  nome: string;
  uf: string;
  empresaId: string;
  status: 'Ativo' | 'Inativo';
}
