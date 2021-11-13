import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Configurations1Component } from './configurations.component';

describe('Configurations1Component', () => {
  let component: Configurations1Component;
  let fixture: ComponentFixture<Configurations1Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ Configurations1Component ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(Configurations1Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
