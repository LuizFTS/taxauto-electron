import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Filiais } from './filiais';

describe('Filiais', () => {
  let component: Filiais;
  let fixture: ComponentFixture<Filiais>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Filiais]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Filiais);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
