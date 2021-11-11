import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { LocalDataSource } from 'ng2-smart-table';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-add-configurations',
  templateUrl: './add-configurations.component.html',
  styleUrls: ['./add-configurations.component.scss'],
})
export class AddConfigurationsComponent implements OnInit {
  destroyByClick = true;
  duration = 2000;
  hasIcon = true;
  preventDuplicates = false;

  source: LocalDataSource = new LocalDataSource();

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router,
  ) {
      // const data = this.http.get(SERVER_API_URL + '/config');
      // this.source.load(data);
   }

  ngOnInit(): void {
  }

  kafkaForm = this.fb.group({
    server: ['', [Validators.required]],
    port: ['', [Validators.required]],
  });

  sparkForm = this.fb.group({
    value: ['', [Validators.required]],
  });

  emailForm = this.fb.group({
    username: ['', [Validators.required]],
    password: ['', [Validators.required]],
  });

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

  onSubmitKafka(): void {
    const addKafka = this.kafkaForm.getRawValue();
    addKafka['value'] = {'bootstrap.servers': addKafka.server + ':' + addKafka.port};
    addKafka['name'] = 'kafka';
    delete addKafka.server;
    delete addKafka.port;
    const res = this.http.post(SERVER_API_URL + '/config', addKafka)
    .subscribe(
      res => {
        this.showToast('Notification', 'Action completed', 'success');
      }, (error) => {
        this.showToast('An unexpected error occured', error.message, 'danger');
      }, () => {},
    );
    this.kafkaForm.reset();
  }

  onSubmitSpark(): void {
    const addSpark = this.sparkForm.getRawValue();
    console.log(addSpark)
    // addSpark['name'] = 'spark';
    // addSpark.value = {'master': addSpark.value};
    // const res = this.http.post(SERVER_API_URL + '/config', addSpark)
    // .subscribe(
    //   res => {
    //     this.showToast('Notification', 'Action completed', 'success');
    //   }, (error) => {
    //     this.showToast('An unexpected error occured', error.message, 'danger');
    //   }, () => {},
    // );
    // this.sparkForm.reset();
  }

  onSubmitEmail(): void {
    const addMail = this.emailForm.getRawValue();
    addMail['value'] = {'username': addMail.username, 'password': addMail.password};
    delete addMail.username;
    delete addMail.password;
    addMail['name'] = 'mail';
    // console.log(Object.getOwnPropertyNames(addMail))
    const res = this.http.post(SERVER_API_URL + '/config', addMail)
    .subscribe(
      res => {
        this.showToast('Notification', 'Action completed', 'success');
      }, (error) => {
        this.showToast('An unexpected error occured', error.message, 'danger');
      }, () => {},
    );
    this.emailForm.reset();
  }

  table = this.fb.group({
    name: new FormControl('', (Validators.required)),
    charset: ['', [Validators.required]],
    collate: ['', [Validators.required]],
    engine: ['InnoDB', [Validators.required]],
    fields: this.fb.array([this.createFieldTable()]),
  });

  get fields(): FormArray {
    return <FormArray> this.table.get('fields');
  }

  createFieldTable(): FormGroup {
    return this.fb.group({
      name_field: [null, [Validators.required]],
      type: [null, [Validators.required]],
      primary_key: [false, [Validators.required]],
      auto_increment: [false, [Validators.required]],
      nullable: [false, [Validators.required]],
      unique: [false, [Validators.required]],
      default: ['', [Validators.required]],
      length: [0, [Validators.required]],
      value: ['', [Validators.required]],
      collation: ['latin1_swedish_ci', [Validators.required]],
      comment: ['', [Validators.required]],
    });
  }

  onReset(): void {
    this.sparkForm.reset();
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



  onDeleteConfirm(event): void {
    // console.log(event['data']['table_name']);
    this.router.navigate([event['data']['table_name']]);
  }

}
