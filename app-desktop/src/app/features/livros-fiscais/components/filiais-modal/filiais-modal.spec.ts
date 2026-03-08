import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FiliaisModal } from './filiais-modal';

describe('FiliaisModal', () => {
  let component: FiliaisModal;
  let fixture: ComponentFixture<FiliaisModal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FiliaisModal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FiliaisModal);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
