import type { StatusPeriodo } from '../types/status-periodo.type';

export interface Periodo {
  id: number | null;
  ano: number;
  mes: number;
  chave: string;
  status: StatusPeriodo;
  criado_em: string | null;
  atualizado_em: string | null;
}
