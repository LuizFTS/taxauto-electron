import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Apuracao } from './apuracao';

describe('Apuracao', () => {
  let component: Apuracao;
  let fixture: ComponentFixture<Apuracao>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Apuracao]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Apuracao);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
