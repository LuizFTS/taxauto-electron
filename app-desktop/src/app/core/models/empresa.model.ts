export interface Empresa {
  id: string;
  numero: string;
  nome: string;
  filiais: string[];
  status: 'Ativo' | 'Inativo';
}
