import type { GrupoEmpresas } from '../../core';
import type { BranchGroupWithBranchesDTO } from '../../core/models/api/response/branch-group-with-branches-response.mode';

export class GroupBranchMapper {
  /**
   * Converte uma única Filial do backend para o formato do Frontend
   */
  static toGroupBranch(branch: BranchGroupWithBranchesDTO): GrupoEmpresas {
    return {
      id: String(branch.id),
      name: branch.name,
      branches: branch.branches.map((branch) => ({
        id: String(branch.id),
        codigo: branch.codigo,
        name: branch.name,
      })),
    };
  }

  static toGroupBranchList(data: BranchGroupWithBranchesDTO[]): GrupoEmpresas[] {
    return data.map((branch) => this.toGroupBranch(branch));
  }
}
