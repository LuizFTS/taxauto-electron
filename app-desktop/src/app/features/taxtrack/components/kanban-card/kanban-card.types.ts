export type KanbanStatus = 'pendente' | 'em_andamento' | 'entregue' | 'atrasado';

export interface KanbanItem {
  id: string;
  title: string;
  category: string;
  location: string;
  statusText: string;
  status: KanbanStatus;
  assigneeAvatarUrl: string;
}
