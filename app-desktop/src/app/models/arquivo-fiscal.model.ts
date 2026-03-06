export type StatusArquivo = 'OK' | 'FAIL' | 'PENDENTE' | 'AUSENTE';

export type TipoArquivo =
  | 'LIVRO_ENTRADA'
  | 'LIVRO_SAIDA'
  | 'DIFAL'
  | 'ST'
  | 'ESTORNO_CREDITO'
  | 'ESTORNO_MERCADORIA_DETERIORADA'
  | 'FOT'
  | 'FRETE_ENTRADA'
  | 'FRETE_SAIDA'
  | 'INEXIGIBILIDADE';

export interface ArquivoFiscal {
  tipo: TipoArquivo;
  label: string;
  nome_arquivo: string | null;
  caminho: string | null;
  status: StatusArquivo;
  obrigatorio: boolean;
  erro_mensagem: string | null;
  total_linhas: number | null;
}

export const TIPOS_ARQUIVO_CONFIG: Record<TipoArquivo, { label: string; obrigatorio: boolean }> = {
  LIVRO_ENTRADA: { label: 'Livro de Entradas', obrigatorio: true },
  LIVRO_SAIDA: { label: 'Livro de Saídas', obrigatorio: true },
  DIFAL: { label: 'DIFAL', obrigatorio: false },
  ST: { label: 'Substituição Tributária (ST)', obrigatorio: false },
  ESTORNO_CREDITO: { label: 'Estorno de Crédito', obrigatorio: false },
  ESTORNO_MERCADORIA_DETERIORADA: { label: 'Estorno - Mercadoria Deteriorada', obrigatorio: false },
  FOT: { label: 'FOT', obrigatorio: false },
  FRETE_ENTRADA: { label: 'Frete de Entrada', obrigatorio: false },
  FRETE_SAIDA: { label: 'Frete de Saída', obrigatorio: false },
  INEXIGIBILIDADE: { label: 'Inexigibilidade', obrigatorio: false },
};
