export type StatusPeriodo =
  | 'CRIADO'
  | 'IMPORTANDO'
  | 'IMPORTADO'
  | 'PROCESSANDO'
  | 'CONCLUIDO'
  | 'ERRO';

export interface Periodo {
  id: number | null;
  ano: number;
  mes: number;
  chave: string;
  status: StatusPeriodo;
  criado_em: string | null;
  atualizado_em: string | null;
}

export interface CriarPeriodoResponse {
  periodo: Periodo;
  workspace_paths: Record<string, string>;
  appdata_paths: Record<string, string>;
  ja_existia: boolean;
  mensagem: string;
}
