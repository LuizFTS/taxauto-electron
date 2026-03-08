import type { StatusArquivo } from '../types/status-arquivo.type';
import type { TipoArquivo } from '../types/tipo-arquivo.type';

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
