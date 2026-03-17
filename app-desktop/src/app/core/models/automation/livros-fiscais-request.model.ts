import type { TaskRequest } from './task-request.model';

export interface LivrosFiscaisRequest {
  start_date: string;
  end_date: string;
  filiais: string[];
  book_type: string;
  consolidado: boolean;
  tasks: TaskRequest;
  save_path?: string | null;
}
