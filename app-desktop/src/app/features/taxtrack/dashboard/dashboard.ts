import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Kanban } from '../components/kanban/kanban';
import { Filters } from '../components/filters/filters';
import { KpiCard } from '../components/kpi-card/kpi-card';
import { KanbanItem } from '../components/kanban-card/kanban-card.types';
import { KpiCardData } from '../components/kpi-card/kpi-card.types';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [Kanban, Filters, KpiCard, ReactiveFormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard {
  private fb = inject(FormBuilder);

  filtersForm: FormGroup = this.fb.group({
    empresa: ['todas'],
    filial: ['todas'],
    responsavel: ['todos'],
    tipo: ['todos'],
    mesAno: ['10/2023'],
  });

  mockKpiCards: KpiCardData[] = [
    { title: 'VENCIDAS', value: '05', icon: 'cancel', type: 'danger' },
    { title: 'VENCE HOJE', value: '03', icon: 'notifications', type: 'warning' },
    { title: 'VENCE EM 1-5 DIAS', value: '12', icon: 'calendar_today', type: 'info' },
    { title: 'RESTANTE DO MÊS', value: '28', icon: 'event_available', type: 'success' },
  ];

  mockKanbanItems: KanbanItem[] = [
    {
      id: '1',
      title: 'Apuração Mensal PIS/COFINS',
      category: 'EFD-CONTRIBUIÇÕES',
      location: 'São Paulo - SP',
      statusText: '15 Out',
      status: 'pendente',
      assigneeAvatarUrl: '',
    },
    {
      id: '2',
      title: 'Declaração de Débitos Federais',
      category: 'DCTF',
      location: 'Curitiba - PR',
      statusText: 'Processando',
      status: 'em_andamento',
      assigneeAvatarUrl: '',
    },
    {
      id: '3',
      title: 'Escrituração Fiscal Retenções',
      category: 'EFD REINF',
      location: 'Belo Horizonte - MG',
      statusText: 'Concluído',
      status: 'entregue',
      assigneeAvatarUrl: '',
    },
    {
      id: '4',
      title: 'Guia de Info. Apuração',
      category: 'GIA MENSAL',
      location: 'Porto Alegre - RS',
      statusText: 'Vencido há 2d',
      status: 'atrasado',
      assigneeAvatarUrl: '',
    },
    {
      id: '5',
      title: 'Geração de Arquivo Magnético',
      category: 'SPED ICMS',
      location: 'Rio de Janeiro - RJ',
      statusText: '20 Out',
      status: 'pendente',
      assigneeAvatarUrl: '',
    },
  ];
}
