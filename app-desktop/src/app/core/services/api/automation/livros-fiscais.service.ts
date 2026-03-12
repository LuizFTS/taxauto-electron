import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import type { LivrosFiscaisRequest } from '../../../models/automation/livros-fiscais-request.model';
import type { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class LivrosFiscaisService {
  private readonly baseUrl = 'http://127.0.0.1:8000/api/v1/livros-fiscais';
  private readonly http: HttpClient = inject(HttpClient);

  execute(request: LivrosFiscaisRequest): Observable<void> {
    return this.http.post<void>(`${this.baseUrl}/run`, request);
  }
}
