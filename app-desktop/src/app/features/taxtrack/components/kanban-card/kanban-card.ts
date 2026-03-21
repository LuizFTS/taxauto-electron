import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { KanbanItem } from './kanban-card.types';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-kanban-card',
  standalone: true,
  imports: [CommonModule, MatIcon],
  templateUrl: './kanban-card.html',
  styleUrl: './kanban-card.scss',
})
export class KanbanCard {
  @Input({ required: true }) item!: KanbanItem;
}
