import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms';

import { LivrosFiscais } from './livros-fiscais';

describe('LivrosFiscais', () => {
  let component: LivrosFiscais;
  let fixture: ComponentFixture<LivrosFiscais>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LivrosFiscais, NoopAnimationsModule, ReactiveFormsModule],
    }).compileComponents();

    fixture = TestBed.createComponent(LivrosFiscais);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
