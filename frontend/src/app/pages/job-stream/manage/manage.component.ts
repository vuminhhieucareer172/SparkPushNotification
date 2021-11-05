import { HttpClient } from '@angular/common/http';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { Observable } from 'rxjs/Rx';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.scss'],
})
export class ManageComponent implements OnInit, OnDestroy {
  hours: any[];
  minutes: number[];
  seconds: number[];
  days: any[];
  schedule: string;
  status = {
    mysql: 'stopped',
    spark: 'stopped',
    kafka: 'stopped',
  };
  destroyByClick = true;
  duration = 2000;
  hasIcon = true;
  preventDuplicates = false;

  jobForm = this.fb.group({
    name_job: ['', (Validators.required)],
    schedule: ['', [Validators.required]],
  });
  private alive: boolean;
  objectKeys = Object.keys;

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService) {
    this.alive = true;
    this.minutes = Array.from(Array(60), (_, i) => i);
    this.seconds = Array.from(Array(60), (_, i) => i);
    this.hours = Array.from(Array(24), (_, i) => i);
    this.days = Array.from(Array(30), (_, i) => i);
  }

  ngOnInit(): void {
    for (let i = 0; i < Object.keys(this.status).length; i++) {
      this.getStatus(Object.keys(this.status)[i]);
    }
  }

  onSelectSchedule(value: string): void {
    this.schedule = value;
  }

  setSchedule(value: string): void {
    this.jobForm.controls['schedule'].setValue(value);
  }

  getStatus(service: string): void {
    Observable.interval(5000)
      .startWith(0)
      .takeWhile(() => this.alive)
      .subscribe((x) => {
        this.http.get(SERVER_API_URL + '/status-' + service)
        .subscribe(
          res => {
            this.status[service] = res['status'];
          }, (error) => {
            this.status[service] = 'stopped';
          }, () => {},
        );
    });
  }

  stopJob(): void {
    this.http.get(SERVER_API_URL + '/stop-job-streaming')
    .subscribe(
      res => {
        this.showToast('Notification', 'Action completed', 'success');
      }, (error) => {
        this.showToast('An unexpected error occured', error.message, 'danger');
      }, () => {},
    );
  }

  runJob(): void {
    this.http.get(SERVER_API_URL + '/start-job-streaming')
    .subscribe(
      res => {
        this.showToast('Notification', 'Action completed', 'success');
      }, (error) => {
        this.showToast('An unexpected error occured', error.message, 'danger');
      }, () => {},
    );
  }

  private showToast(title: string, body: string, typeStatus: string) {
    const config = {
      status: typeStatus,
      destroyByClick: this.destroyByClick,
      duration: this.duration,
      hasIcon: this.hasIcon,
      position: NbGlobalPhysicalPosition.TOP_RIGHT,
      preventDuplicates: this.preventDuplicates,
    };
    const titleContent = title ? title : 'error';

    this.toastrService.show(
      body,
      titleContent,
      config);
  }

  onSubmit(): void {
    const jobInfo = this.jobForm.getRawValue();
    const res = this.http.post(SERVER_API_URL + '/update-job-streaming', jobInfo)
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.message, 'danger');
        }, () => {},
    );
  }

  ngOnDestroy(): void {
    this.alive = false;
  }
}
