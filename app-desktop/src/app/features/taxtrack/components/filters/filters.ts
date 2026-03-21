import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';
import { Select, SelectOption } from '../../../../shared/components/select/select';
import { Card } from '../../../../shared/components/card/card';

@Component({
  selector: 'app-filters',
  standalone: true,
  imports: [CommonModule, Select, ReactiveFormsModule, Card],
  templateUrl: './filters.html',
  styleUrl: './filters.scss',
})
export class Filters {
  @Input({ required: true }) form!: FormGroup;

  empresasOptions: SelectOption[] = [{ label: 'Todas as Empresas', value: 'todas' }];

  filiaisOptions: SelectOption[] = [{ label: 'Todas as Filiais', value: 'todas' }];

  responsaveisOptions: SelectOption[] = [{ label: 'Todos', value: 'todos' }];

  tiposOptions: SelectOption[] = [{ label: 'Todos os Tributos', value: 'todos' }];

  mesAnoOptions: SelectOption[] = [{ label: 'Out/2023', value: '10/2023' }];
}
