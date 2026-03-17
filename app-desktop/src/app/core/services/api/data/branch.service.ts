import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { CreateBranchRequest } from '../../../models/api/request/create-branch.model';
import type { BranchResponse } from '../../../models/api/response/branch-response.model';
import { BackendService } from '../backend.service';

@Injectable({ providedIn: 'root' })
export class BranchService {
  private http = inject(HttpClient);
  private backend = inject(BackendService);

  createBranch(branch: CreateBranchRequest): Observable<BranchResponse> {
    return this.http.post<BranchResponse>(`${this.backend.api}/branches/`, branch);
  }

  getAll(): Observable<BranchResponse[]> {
    return this.http.get<BranchResponse[]>(`${this.backend.api}/branches/`);
  }

  getById(id: number): Observable<BranchResponse> {
    return this.http.get<BranchResponse>(`${this.backend.api}/branches/${id}`);
  }

  updateBranch(
    id: number,
    {
      name,
      uf,
      cnpj,
      ie,
      company_id,
      status,
    }: { name: string; uf: string; cnpj: string; ie: string; company_id: number; status: boolean },
  ): Observable<void> {
    return this.http.patch<void>(`${this.backend.api}/branches/${id}`, {
      name,
      uf,
      cnpj,
      ie,
      company_id,
      ativa: status,
    });
  }

  deleteBranch(id: number): Observable<void> {
    return this.http.delete<void>(`${this.backend.api}/branches/${id}`);
  }
}
