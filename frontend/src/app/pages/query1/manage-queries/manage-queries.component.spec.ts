import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageQueriesComponent } from './manage-queries.component';

describe('ManageQueriesComponent', () => {
  let component: ManageQueriesComponent;
  let fixture: ComponentFixture<ManageQueriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageQueriesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageQueriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
