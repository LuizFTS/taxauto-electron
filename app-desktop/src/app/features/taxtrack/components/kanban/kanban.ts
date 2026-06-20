import { Component, Input, OnInit, OnChanges } from '@angular/core';
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
export class Kanban implements OnInit, OnChanges {
  @Input() items: KanbanItem[] = [];

  columns: KanbanColumn[] = [
    { title: 'Vencidas', status: 'atrasado', items: [] },
    { title: 'Vence Hoje', status: 'atrasado', items: [] },
    { title: 'A Vencer', status: 'em_andamento', items: [] },
    { title: 'Entregues', status: 'entregue', items: [] },
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
