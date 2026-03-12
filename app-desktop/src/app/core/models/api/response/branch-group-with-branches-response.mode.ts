import type { BranchGroupResponseDTO } from './branch-group-response.model';

export interface BranchGroupWithBranchesDTO {
  id: number;
  name: string;
  analyst: string;
  branches: BranchGroupResponseDTO[];
}
