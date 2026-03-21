import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { KanbanCard } from '../kanban-card/kanban-card';
import { KanbanItem, KanbanStatus } from '../kanban-card/kanban-card.types';

interface KanbanColumn {
  title: string;
  status: KanbanStatus;
  items: KanbanItem[];
}

@Component({
  selector: 'app-kanban',
  standalone: true,
  imports: [CommonModule, KanbanCard],
  templateUrl: './kanban.html',
  styleUrl: './kanban.scss',
})
export class Kanban implements OnInit {
  @Input() items: KanbanItem[] = [];

  columns: KanbanColumn[] = [
    { title: 'Pendente', status: 'pendente', items: [] },
    { title: 'Em Andamento', status: 'em_andamento', items: [] },
    { title: 'Entregue', status: 'entregue', items: [] },
    { title: 'Atrasado', status: 'atrasado', items: [] },
  ];

  ngOnInit() {
    this.distributeItems();
  }

  ngOnChanges() {
    this.distributeItems();
  }

  private distributeItems() {
    this.columns.forEach((col) => {
      col.items = this.items.filter((item) => item.status === col.status);
    });
  }
}
