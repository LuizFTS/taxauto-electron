import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WindowLayout } from './window-layout';

describe('WindowLayout', () => {
  let component: WindowLayout;
  let fixture: ComponentFixture<WindowLayout>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WindowLayout]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WindowLayout);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
