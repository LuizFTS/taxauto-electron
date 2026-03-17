import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { Empresa } from '../../../models/empresa.model';
import type { CreateCompanyRequest } from '../../../models/api/request/create-company.model';
import type { CompanyResponse } from '../../../models/api/response/company-response.model';
import { BackendService } from '../backend.service';

@Injectable({ providedIn: 'root' })
export class CompanyService {
  private http = inject(HttpClient);
  private backend = inject(BackendService);

  createCompany(company: CreateCompanyRequest): Observable<Empresa> {
    return this.http.post<Empresa>(`${this.backend.api}/companies/`, company);
  }

  getAll(): Observable<CompanyResponse[]> {
    return this.http.get<CompanyResponse[]>(`${this.backend.api}/companies/`);
  }

  getById(id: number): Observable<CompanyResponse> {
    return this.http.get<CompanyResponse>(`${this.backend.api}/companies/${id}`);
  }

  updateCompany(id: number, name: string, status: boolean): Observable<void> {
    return this.http.patch<void>(`${this.backend.api}/companies/${id}`, {
      name: name,
      ativa: status,
    });
  }

  deleteCompany(id: number): Observable<void> {
    return this.http.delete<void>(`${this.backend.api}/companies/${id}`);
  }
}
