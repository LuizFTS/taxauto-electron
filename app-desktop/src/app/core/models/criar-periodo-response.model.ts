import type { Periodo } from './periodo.model';

export interface CriarPeriodoResponse {
  periodo: Periodo;
  workspace_paths: Record<string, string>;
  appdata_paths: Record<string, string>;
  ja_existia: boolean;
  mensagem: string;
}
