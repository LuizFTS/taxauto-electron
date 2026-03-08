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
