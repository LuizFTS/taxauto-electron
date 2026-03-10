// src/shared/mappers/company.mapper.ts

import type { CompanyResponse } from '../../core/models/api/response/company-response.model';
import type { BranchResponse } from '../../core/models/api/response/branch-response.model';
import type { Empresa } from '../../core/models/empresa.model';
import type { Filial } from '../../core/models/filial.model';

export class CompanyMapper {
  /**
   * Converte uma única Filial do backend para o formato do Frontend
   */
  static toFilial(branch: BranchResponse, empresaAtiva = true): Filial {
    return {
      id: String(branch.id),
      numero: branch.codigo.padStart(3, '0'),
      nome: branch.nome,
      uf: branch.uf,
      empresaId: String(branch.company_id),
      status: empresaAtiva ? 'Ativo' : 'Inativo',
    };
  }

  /**
   * Converte uma LISTA de Filiais
   * Útil para listagens isoladas de filiais
   */
  static toFilialList(branches: BranchResponse[], empresas: CompanyResponse[]): Filial[] {
    return branches.map((branch) => {
      // Busca a empresa correspondente para saber o status
      const empresa = empresas.find((e) => e.id === branch.company_id);
      return this.toFilial(branch, empresa?.ativa ?? true);
    });
  }

  /**
   * Converte uma única Empresa (com suas filiais) para o formato do Frontend
   */
  static toEmpresa(company: CompanyResponse, allBranches: BranchResponse[]): Empresa {
    const filiaisDaEmpresa = allBranches
      .filter((b) => b.company_id === company.id)
      .map((b) => this.toFilial(b, company.ativa));

    return {
      id: String(company.id),
      numero: company.codigo.padStart(3, '0'),
      nome: company.nome,
      status: company.ativa ? 'Ativo' : 'Inativo',
      filiais: filiaisDaEmpresa,
    };
  }

  /**
   * Converte LISTAS completas vindas do backend
   */
  static toEmpresaList(companies: CompanyResponse[], branches: BranchResponse[]): Empresa[] {
    return companies.map((company) => this.toEmpresa(company, branches));
  }
}
