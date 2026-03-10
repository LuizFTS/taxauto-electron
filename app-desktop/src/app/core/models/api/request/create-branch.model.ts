export interface CreateBranchRequest {
  codigo: string;
  nome: string;
  uf: string;
  cnpj: string;
  ie: string | null;
  company_id: number;
}
