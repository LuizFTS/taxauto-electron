import { Component, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TaxReportsService } from '../../../../../core/services/api/automation/tax-reports.service';

@Component({
  selector: 'app-workflow',
  imports: [],
  templateUrl: './workflow.html',
  styleUrl: './workflow.scss',
})
export class Workflow {
  private route = inject(ActivatedRoute);

  private taxReportsService = inject(TaxReportsService);

  readonly start_date = this.route.snapshot.queryParams['start_date'];
  readonly end_date = this.route.snapshot.queryParams['end_date'];
  readonly filiais = this.route.snapshot.queryParams['filiais'];

  /**
   *
   */

  private updateBooks(start_date: string, end_date: string, filiais: string[]) {
    this.taxReportsService.execute({
      start_date,
      end_date,
      filiais,
      book_type: 'saida',
      tasks: {
        open_book: false,
        update_book: true,
        close_book: false,
        save_spreadsheet: false,
        save_pdf: false,
      },
      save_path: null,
    });
  }
}
