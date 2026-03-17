import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { CreateBranchGroupRequest } from '../../../models/api/request/create-branch-group.model';
import type { BranchGroupResponseDTO } from '../../../models/api/response/branch-group-response.model';
import type { BranchGroupWithBranchesDTO } from '../../../models/api/response/branch-group-with-branches-response.mode';
import { BackendService } from '../backend.service';

@Injectable({ providedIn: 'root' })
export class BranchGroupService {
  private http = inject(HttpClient);
  private backend = inject(BackendService);

  createBranchGroup(branch: CreateBranchGroupRequest): Observable<BranchGroupResponseDTO> {
    return this.http.post<BranchGroupResponseDTO>(`${this.backend.api}/branch-group/`, branch);
  }

  addBranchInGroup(group_id: number, branch_id: number): Observable<void> {
    return this.http.post<void>(
      `${this.backend.api}/branch-group/${group_id}/branches/${branch_id}`,
      {},
    );
  }

  getAll(): Observable<BranchGroupWithBranchesDTO[]> {
    return this.http.get<BranchGroupWithBranchesDTO[]>(`${this.backend.api}/branch-group/`);
  }

  getById(id: number): Observable<BranchGroupWithBranchesDTO> {
    return this.http.get<BranchGroupWithBranchesDTO>(`${this.backend.api}/branch-group/${id}`);
  }

  updateBranchGroup(id: number, branch: BranchGroupResponseDTO): Observable<void> {
    return this.http.put<void>(`${this.backend.api}/branch-group/${id}`, branch);
  }

  deleteBranchGroup(id: number): Observable<void> {
    return this.http.delete<void>(`${this.backend.api}/branch-group/${id}`);
  }
}
