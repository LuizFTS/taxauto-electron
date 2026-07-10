import type { FlowTask } from '../../../shared/components/flow-tasks-modal/flow-tasks-modal';

export interface SelectOptions {
  value: number;
  label: string;
}

export interface Tarefa {
  id: string;
  nome: string;
}

export interface LivroFiscalPayload {
  book_type: BookType;
  start_date: string;
  end_date: string;
  filiais: string[];
  save_path: string | null;
  tasks: {
    open_book: boolean;
    update_book: boolean;
    close_book: boolean;
    save_spreadsheet: boolean;
    save_pdf: boolean;
  };
}

export type TarefaId = 'atualizar' | 'abrir' | 'fechar' | 'salvar_excel' | 'salvar_pdf';

export type TipoRelatorioId = 1 | 2 | 3 | 4 | 5;

export interface CancelledInvoicesPayload {
  start_date: string;
  end_date: string;
  filiais: string[];
  save_path: string;
  login: string;
  password: string;
}
export interface CancelledInvoicesFlowPayload {
  start_date: string;
  end_date: string;
  filiais: string[];
  login: string;
  password: string;
  tasks: FlowTask[];
}
export interface DownloadXmlsPayload {
  start_date: string;
  end_date: string;
  filiais: string[];
  save_path: string;
  login: string;
  password: string;
  tipo_documento: number;
  tipo_operacao: number;
}

export type BookType = 'entrada' | 'saida';
