import { Component, signal } from '@angular/core';
import { RouterOutlet, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
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
