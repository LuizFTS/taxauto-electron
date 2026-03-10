import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { Empresa } from '../../../models/empresa.model';
import type { CreateCompanyRequest } from '../../../models/api/request/create-company.model';
import type { CompanyResponse } from '../../../models/api/response/company-response.model';

const API = 'http://127.0.0.1:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class CompanyService {
  private http = inject(HttpClient);

  createCompany(company: CreateCompanyRequest): Observable<Empresa> {
    return this.http.post<Empresa>(`${API}/companies/`, company);
  }

  getAll(): Observable<CompanyResponse[]> {
    return this.http.get<CompanyResponse[]>(`${API}/companies/`);
  }

  getById(id: number): Observable<CompanyResponse> {
    return this.http.get<CompanyResponse>(`${API}/companies/${id}`);
  }

  updateCompany(id: number, company: CompanyResponse): Observable<CompanyResponse> {
    return this.http.put<CompanyResponse>(`${API}/companies/${id}`, company);
  }

  deleteCompany(id: number): Observable<CompanyResponse> {
    return this.http.delete<CompanyResponse>(`${API}/companies/${id}`);
  }
}
