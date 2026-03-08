export interface ProcessamentoStatus {
  etapa: string;
  progresso: number; // 0–100
  mensagem: string;
  concluido: boolean;
  erro: string | null;
}
