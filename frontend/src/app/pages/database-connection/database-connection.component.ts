import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, Validators, FormGroup, FormArray, FormControl } from '@angular/forms';
import { SERVER_API_URL } from '../../app.constants';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';


@Component({
  selector: 'ngx-database-connection',
  styleUrls: ['./database-connection.component.scss'],
  templateUrl: './database-connection.component.html',
})
export class DatabaseConnectionComponent implements OnInit {
  destroyByClick = true;
  duration = 5000;
  hasIcon = true;
  preventDuplicates = false;

  dbForm = this.fb.group({
    db_driver: ['mysql', (Validators.required)],
    db_host: ['localhost', [Validators.required]],
    db_port: [3306, [Validators.required]],
    db_name: ['', [Validators.required]],
    db_username: ['', [Validators.required]],
    db_password: ['', [Validators.required]],
    db_driver_manager: [''],
  });

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService) {
  }

  ngOnInit(): void {
    this.http.get(SERVER_API_URL + '/connect-database')
    .subscribe(
      res => {
        this.dbForm.controls['db_driver'].setValue(res['drivername']);
        this.dbForm.controls['db_host'].setValue(res['host']);
        this.dbForm.controls['db_port'].setValue(res['port']);
        this.dbForm.controls['db_name'].setValue(res['database']);
        this.dbForm.controls['db_username'].setValue(res['username']);
        this.dbForm.controls['db_password'].setValue(res['password']);
      },
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

  onReset(): void {
    this.dbForm.reset();
  }
// c
  onTestSubmit(): void {
    const stream = this.dbForm.getRawValue();
    this.http.post(SERVER_API_URL + '/test-connect-database', stream, {observe: 'response'})
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => {},
    );
  }

  onSubmit(): void {
    const stream = this.dbForm.getRawValue();
    this.http.post(SERVER_API_URL + '/connect-database', stream, {observe: 'response'})
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => {},
    );
  }

}
