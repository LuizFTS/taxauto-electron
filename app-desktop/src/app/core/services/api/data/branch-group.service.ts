import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { CreateBranchGroupRequest } from '../../../models/api/request/create-branch-group.model';
import type { BranchGroupResponse } from '../../../models/api/response/branch-group-response.mode';

const API = 'http://127.0.0.1:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class BranchGroupService {
  private http = inject(HttpClient);

  createBranchGroup(branch: CreateBranchGroupRequest): Observable<BranchGroupResponse> {
    return this.http.post<BranchGroupResponse>(`${API}/branch-group/`, branch);
  }

  getAll(): Observable<BranchGroupResponse[]> {
    return this.http.get<BranchGroupResponse[]>(`${API}/branch-group/`);
  }

  getById(id: number): Observable<BranchGroupResponse> {
    return this.http.get<BranchGroupResponse>(`${API}/branch-group/${id}`);
  }

  updateBranchGroup(id: number, branch: BranchGroupResponse): Observable<BranchGroupResponse> {
    return this.http.put<BranchGroupResponse>(`${API}/branch-group/${id}`, branch);
  }

  deleteBranchGroup(id: number): Observable<BranchGroupResponse> {
    return this.http.delete<BranchGroupResponse>(`${API}/branch-group/${id}`);
  }
}
