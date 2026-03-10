import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { CreateBranchRequest } from '../../../models/api/request/create-branch.model';
import type { BranchResponse } from '../../../models/api/response/branch-response.model';

const API = 'http://127.0.0.1:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class BranchService {
  private http = inject(HttpClient);

  createBranch(branch: CreateBranchRequest): Observable<BranchResponse> {
    return this.http.post<BranchResponse>(`${API}/branches/`, branch);
  }

  getAll(): Observable<BranchResponse[]> {
    return this.http.get<BranchResponse[]>(`${API}/branches/`);
  }

  getById(id: number): Observable<BranchResponse> {
    return this.http.get<BranchResponse>(`${API}/branches/${id}`);
  }

  updateBranch(id: number, branch: BranchResponse): Observable<BranchResponse> {
    return this.http.put<BranchResponse>(`${API}/branches/${id}`, branch);
  }

  deleteBranch(id: number): Observable<BranchResponse> {
    return this.http.delete<BranchResponse>(`${API}/branches/${id}`);
  }
}
