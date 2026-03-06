import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Difal } from './difal';

describe('Difal', () => {
  let component: Difal;
  let fixture: ComponentFixture<Difal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Difal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Difal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
