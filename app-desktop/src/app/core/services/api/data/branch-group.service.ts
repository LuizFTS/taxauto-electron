import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { CreateBranchGroupRequest } from '../../../models/api/request/create-branch-group.model';
import type { BranchGroupResponseDTO } from '../../../models/api/response/branch-group-response.model';
import type { BranchGroupWithBranchesDTO } from '../../../models/api/response/branch-group-with-branches-response.mode';

const API = 'http://127.0.0.1:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class BranchGroupService {
  private http = inject(HttpClient);

  createBranchGroup(branch: CreateBranchGroupRequest): Observable<BranchGroupResponseDTO> {
    return this.http.post<BranchGroupResponseDTO>(`${API}/branch-group/`, branch);
  }

  addBranchInGroup(group_id: number, branch_id: number): Observable<void> {
    return this.http.post<void>(`${API}/branch-group/${group_id}/branches/${branch_id}`, {});
  }

  getAll(): Observable<BranchGroupWithBranchesDTO[]> {
    return this.http.get<BranchGroupWithBranchesDTO[]>(`${API}/branch-group/`);
  }

  getById(id: number): Observable<BranchGroupWithBranchesDTO> {
    return this.http.get<BranchGroupWithBranchesDTO>(`${API}/branch-group/${id}`);
  }

  updateBranchGroup(id: number, branch: BranchGroupResponseDTO): Observable<void> {
    return this.http.put<void>(`${API}/branch-group/${id}`, branch);
  }

  deleteBranchGroup(id: number): Observable<void> {
    return this.http.delete<void>(`${API}/branch-group/${id}`);
  }
}
