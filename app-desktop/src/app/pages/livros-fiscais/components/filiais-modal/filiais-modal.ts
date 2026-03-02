import {
  Component,
  inject,
  Input,
  ViewChild,
  type AfterViewInit,
  type ElementRef,
} from '@angular/core';
import { ModalService } from '../../../../services/modal.service';

@Component({
  standalone: true,
  selector: 'app-filiais-modal',
  templateUrl: './filiais-modal.html',
  styleUrl: './filiais-modal.scss',
})
export class FiliaisModal {
  @Input() title: string = 'Filiais';
  @Input() subtitle: string = 'Selecione as filiais';

  private modalService = inject(ModalService);

  confirm() {
    this.modalService.close();
  }

  cancel() {
    this.modalService.close();
  }
}
