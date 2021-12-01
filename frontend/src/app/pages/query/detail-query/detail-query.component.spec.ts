import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetailQueryComponent } from './detail-query.component';

describe('DetailQueryComponent', () => {
  let component: DetailQueryComponent;
  let fixture: ComponentFixture<DetailQueryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DetailQueryComponent ],
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DetailQueryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
