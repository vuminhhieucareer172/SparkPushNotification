import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobStreamComponent } from './job-stream.component';

describe('JobStreamComponent', () => {
  let component: JobStreamComponent;
  let fixture: ComponentFixture<JobStreamComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ JobStreamComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(JobStreamComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
