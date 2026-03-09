import { Component, signal, OnInit, inject } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { Modal } from './shared/components/modal/modal';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Modal],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  private readonly router = inject(Router);
  protected readonly title = signal('app-desktop');

  ngOnInit(): void {
    this.router.navigate(['livros-fiscais']);
  }
}
