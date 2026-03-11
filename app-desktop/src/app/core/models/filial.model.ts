export interface Filial {
  id: string;
  numero: string;
  nome: string;
  uf: string;
  cnpj: string;
  ie: string;
  empresaId: string;
  status: 'Ativo' | 'Inativo';
}
