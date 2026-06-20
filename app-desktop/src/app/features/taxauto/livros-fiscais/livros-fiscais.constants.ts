import { TarefaId, Tarefa, type TipoRelatorioId, type SelectOptions } from './livros-fiscais.types';

export const TIPOS_RELATORIO: SelectOptions[] = [
  { value: 1, label: 'Livro de Entrada' },
  { value: 2, label: 'Livro de Saída' },
  { value: 3, label: 'Notas Canceladas - PortalGED' },
  { value: 4, label: 'Download XMLs' },
  /* { value: 4, label: 'Fluxo: Notas Canceladas' }, */
];

export const TAREFAS_DISPONIVEIS: Tarefa[] = [
  { id: 'atualizar', nome: 'Atualizar livro' },
  { id: 'abrir', nome: 'Abrir livro' },
  { id: 'fechar', nome: 'Fechar livro' },
  { id: 'salvar_excel', nome: 'Salvar Excel' },
  { id: 'salvar_pdf', nome: 'Salvar PDF' },
];

// Tarefas que exigem seleção de pasta de destino
export const TAREFAS_COM_DESTINO = new Set<TarefaId>(['salvar_excel', 'salvar_pdf']);

export const TIPOS_RELATORIO_COM_DESTINO = new Set<TipoRelatorioId>([3, 4]);

export const TIPOS_OPERACAO: SelectOptions[] = [
  { value: 2, label: 'Entrada' },
  { value: 1, label: 'Saída' },
];

export const TIPOS_DOCUMENTO: SelectOptions[] = [
  { value: 1, label: 'NF-e' },
  { value: 2, label: 'CT-e' },
];
