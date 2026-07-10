import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import type { Observable } from 'rxjs';
import { BackendService } from '../backend.service';
import type { DownloadXMLsRequest } from '../../../models/automation/download-xmls-request.model';

@Injectable({ providedIn: 'root' })
export class DownloadXmlsService {
  private readonly http: HttpClient = inject(HttpClient);
  private readonly backend = inject(BackendService);

  execute(request: DownloadXMLsRequest): Observable<void> {
    return this.http.post<void>(`${this.backend.api}/automation/download-xmls/run`, request);
  }
}
