export interface ApuracaoDetalhe {
  tipo: string;
  cfop: string;
  cst: string;
  base_calculo: number;
  aliquota: number;
  valor_icms: number;
  natureza: 'CREDITO' | 'DEBITO';
}
