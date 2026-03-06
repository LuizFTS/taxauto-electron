export interface ApuracaoFilial {
  filial_codigo: string;
  filial_nome: string;
  uf: string;
  total_creditos: number;
  total_debitos: number;
  saldo_credor: number;
  icms_a_recolher: number;
  status: 'OK' | 'ERRO' | 'PENDENTE';
  periodo_chave: string;
}

export interface ApuracaoDetalhe {
  tipo: string;
  cfop: string;
  cst: string;
  base_calculo: number;
  aliquota: number;
  valor_icms: number;
  natureza: 'CREDITO' | 'DEBITO';
}

export interface ProcessamentoStatus {
  etapa: string;
  progresso: number; // 0–100
  mensagem: string;
  concluido: boolean;
  erro: string | null;
}
