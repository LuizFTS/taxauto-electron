import { TarefaId, Tarefa, TipoRelatorio } from './livros-fiscais.types';

export const TIPOS_RELATORIO: TipoRelatorio[] = [
  { value: 1, label: 'Livro de Entrada' },
  { value: 2, label: 'Livro de Saída' },
  { value: 3, label: 'Notas Canceladas - PortalGED' },
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
