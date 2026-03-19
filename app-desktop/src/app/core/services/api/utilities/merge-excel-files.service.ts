import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BackendService } from '../backend.service';
import { Observable } from 'rxjs';
import { MergeExcelFilesRequest } from '../../../models/automation/merge-excel-files-request.model';

@Injectable({ providedIn: 'root' })
export class MergeExcelFilesService {
  private readonly http: HttpClient = inject(HttpClient);
  private readonly backend = inject(BackendService);

  execute(request: MergeExcelFilesRequest): Observable<void> {
    return this.http.post<void>(`${this.backend.api}/utilities/merge-excel-files/run`, request);
  }
}
