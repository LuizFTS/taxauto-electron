import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { KpiCardData } from './kpi-card.types';

@Component({
  selector: 'app-kpi-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './kpi-card.html',
  styleUrl: './kpi-card.scss',
})
export class KpiCard {
  @Input({ required: true }) data!: KpiCardData;
}
