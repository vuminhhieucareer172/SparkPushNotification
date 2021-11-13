import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { LocalDataSource } from 'ng2-smart-table';
import { SERVER_API_URL } from '../../app.constants';

@Component({
  selector: 'ngx-configurations',
  templateUrl: './configurations.component.html',
  styleUrls: ['./configurations.component.scss']
})
export class ConfigurationsComponent implements OnInit {

  destroyByClick = true;
  duration = 2000;
  hasIcon = true;
  preventDuplicates = false;
  show: boolean = false;
  source: LocalDataSource = new LocalDataSource();

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router,) {
    this.http.get(SERVER_API_URL + '/config/kafka', { observe: 'response' })
      .subscribe(
        res => {
          if (res.body != null) {
            this.kafkaForm.controls['server'].setValue(res.body['value']['bootstrap.servers'].split(':')[0]);
            this.kafkaForm.controls['port'].setValue(res.body['value']['bootstrap.servers'].split(':')[1]);
          }
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => { },
      );
    this.http.get(SERVER_API_URL + '/config/mail', { observe: 'response' })
      .subscribe(
        res => {
          if (res.body != null) {
            this.emailForm.controls['hostname'].setValue(res.body['value']['hostname']);
            this.emailForm.controls['port'].setValue(res.body['value']['port']);
            this.emailForm.controls['username'].setValue(res.body['value']['username']);
            this.emailForm.controls['password'].setValue(res.body['value']['password']);
            this.emailForm.controls['mailname'].setValue(res.body['value']['mailname']);
          }
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => { },
      );
    this.http.get(SERVER_API_URL + '/config/spark', { observe: 'response' })
      .subscribe(
        res => {
          let more_config = [];
          this.sparkForm.controls['master'].setValue(res.body['value']['master']);
          this.sparkForm.controls['ip'].setValue(res.body['value']['ip']);
          Object.entries(res.body['value']['more.config']).forEach(
            ([key, value]) => more_config.push({ 'optionConfig': key, 'valueConfig': value })
          );
          more_config.forEach(e => {
            this.fields.push(this.createFieldTable(e['optionConfig'], e['valueConfig']));
          });
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => { },
      );
  }

  ngOnInit(): void {
  }

  password() {
    this.show = !this.show;
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

  sparkForm = this.fb.group({
    master: ['', [Validators.required]],
    ip: ['', [Validators.required]],
    fields: this.fb.array([]),
  });

  get fields(): FormArray {
    return <FormArray>this.sparkForm.get('fields');
  }

  createFieldTable(optionConfig: string = null, valueConfig: string = null): FormGroup {
    return this.fb.group({
      optionConfig: [optionConfig, [Validators.required]],
      valueConfig: [valueConfig, [Validators.required]],
    });
  }

  onSubmitSpark(): void {
    const addSpark = this.sparkForm.getRawValue();
    console.log(addSpark);
    let json_result = {};
    let result = {};
    let more_config = {};
    json_result['name'] = 'spark';
    result["master"] = addSpark.master;
    result["ip"] = addSpark.ip;

    for (var objectConfig of addSpark.fields) {
      more_config[objectConfig['optionConfig']] = objectConfig['valueConfig'];
    };
    result['more.config'] = more_config
    json_result['value'] = result;
    this.http.put(SERVER_API_URL + '/config', json_result, { observe: 'response' })
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => { },
      );
  }

  kafkaForm = this.fb.group({
    server: ['', [Validators.required]],
    port: ['', [Validators.required]],
  });

  onSubmitKafka(): void {
    const addKafka = this.kafkaForm.getRawValue();
    addKafka['value'] = { 'bootstrap.servers': addKafka.server + ':' + addKafka.port };
    addKafka['name'] = 'kafka';
    delete addKafka.server;
    delete addKafka.port;
    const res = this.http.put(SERVER_API_URL + '/config', addKafka)
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.message, 'danger');
        }, () => { },
      );
  }

  emailForm = this.fb.group({
    hostname: ['', [Validators.required]],
    port: ['', [Validators.required]],
    username: ['', [Validators.required]],
    password: ['', [Validators.required]],
    mailname: ['', [Validators.required]],
  });

  onSubmitEmail(): void {
    const addMail = this.emailForm.getRawValue();
    addMail['value'] = {'hostname': addMail.hostname, 'port': addMail.port, 'username': addMail.username, 'password': addMail.password, 'mailname': addMail.mailname };
    delete addMail.username;
    delete addMail.password;
    delete addMail.hostname;
    delete addMail.port;
    delete addMail.mailname;
    addMail['name'] = 'mail';
    const res = this.http.put(SERVER_API_URL + '/config', addMail)
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.message, 'danger');
        }, () => { },
      );
    // this.emailForm.reset();
  }

  addColumn() {
    this.fields.push(this.createFieldTable());
  }

  dropColumn(index: number) {
    this.fields.removeAt(index);
  }

  clearTable() {
    this.fields.clear();
  }

}
