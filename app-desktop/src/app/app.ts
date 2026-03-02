import { Component, signal } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';
import { Modal } from './components/modal/modal';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Modal],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('app-desktop');

  constructor(private readonly router: Router) {}

  ngOnInit(): void {
    this.router.navigate(['livros-fiscais']);
  }
}
