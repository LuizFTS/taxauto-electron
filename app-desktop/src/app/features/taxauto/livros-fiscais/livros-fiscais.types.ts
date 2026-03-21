export interface TipoRelatorio {
  value: number;
  label: string;
}

export interface Tarefa {
  id: string;
  nome: string;
}

export interface LivroFiscalPayload {
  book_type: 'entrada' | 'saida';
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

export interface CancelledInvoicesPayload {
  start_date: string;
  end_date: string;
  filiais: string[];
  save_path: string;
  login: string;
  password: string;
}
