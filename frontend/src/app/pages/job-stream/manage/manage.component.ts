import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.scss'],
})
export class ManageComponent implements OnInit {
  schedule: string;
  status = {
    mysql: 'stopped',
    spark: 'stopped',
    kafka: 'stopped',
  };
  statusJob: string = 'stopped';
  portJob: number = null;
  destroyByClick = true;
  duration = 5000;
  hasIcon = true;
  preventDuplicates = false;

  jobForm = this.fb.group({
    name_job: ['dbstreaming', (Validators.required)],
    schedule: ['', [Validators.required]],
  });
  objectKeys = Object.keys;

  constructor(
    private router: Router,
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService) {
    this.portJob = null;
  }

  ngOnInit(): void {
    for (let i = 0; i < Object.keys(this.status).length; i++) {
      this.getStatus(Object.keys(this.status)[i]);
    }
    this.http.get(SERVER_API_URL + '/job-streaming', {observe: 'response'})
      .subscribe(
        res => {
          this.statusJob = res.body['status'];
          this.setSchedule(res.body['schedule']);
          this.onSelectSchedule('manual-schedule');
          this.portJob = res.body['port'];
        }, (error) => {
          this.statusJob = 'stopped';
        }, () => {},
      );
  }

  navigateSparkUI(): void {
    window.open('http://localhost:4040', '_blank').focus();
  }

  navigateJobLog(): void {
    window.open('http://localhost:5005/static/log-job-dbstreaming/dbstreaming.log', '_blank').focus();
  }

  onSelectSchedule(value: string): void {
    this.schedule = value;
  }

  setSchedule(value: string): void {
    this.jobForm.controls['schedule'].setValue(value);
  }

  getStatus(service: string): void {
    this.http.get(SERVER_API_URL + '/status-' + service, {observe: 'response'})
    .subscribe(
      res => {
        this.status[service] = res.body['status'];
      }, (error) => {
        this.status[service] = 'stopped';
      }, () => {},
    );
  }

  stopJob(): void {
    this.http.get(SERVER_API_URL + '/stop-job-streaming', {observe: 'response'})
    .subscribe(
      res => {
        this.showToast('Notification', 'Action completed', 'success');
      }, (error) => {
        this.showToast('An unexpected error occured', error.error.message, 'danger');
      }, () => {},
    );
  }

  runJob(): void {
    this.http.get(SERVER_API_URL + '/start-job-streaming', {observe: 'response'})
    .subscribe(
      res => {
        this.showToast('Notification', 'Action completed', 'success');
      }, (error) => {
        this.showToast('An unexpected error occured', error.error.message, 'danger');
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
    this.http.post(SERVER_API_URL + '/update-job-streaming', jobInfo, {observe: 'response'})
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => {},
    );
  }
}
