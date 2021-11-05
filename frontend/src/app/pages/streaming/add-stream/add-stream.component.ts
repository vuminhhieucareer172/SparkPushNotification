import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, Validators, FormGroup, FormArray, FormControl } from '@angular/forms';
import { SERVER_API_URL } from '../../../app.constants';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';

@Component({
  selector: 'ngx-add-stream',
  templateUrl: './add-stream.component.html',
  styleUrls: ['./add-stream.component.scss'],
})
export class AddStreamComponent implements OnInit {
  listTopicKafka: string[];
  messageSample: string;
  destroyByClick = true;
  duration = 2000;
  hasIcon = true;
  preventDuplicates = false;

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService) {
    this.messageSample = '';
    this.http.get(SERVER_API_URL + '/kafka-topic')
    .subscribe(
      res => {
        this.listTopicKafka = Object.keys(res).map((key) => res[key]);
      }, (error) => {
        this.showToast('An unexpected error occured', error.message, 'danger');
      }, () => {},
    );
  }

  table = this.fb.group({
    name: new FormControl('', (Validators.required)),
    charset: ['', [Validators.required]],
    collate: ['', [Validators.required]],
    engine: ['InnoDB', [Validators.required]],
    fields: this.fb.array([this.createFieldTable()]),
  });

  streamForm = this.fb.group({
    topic_kafka_input: ['', [Validators.required]],
    table: this.table,
  });

  ngOnInit(): void {
  }

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

  addColumn() {
    this.fields.push(this.createFieldTable());
  }

  dropColumn(index: number) {
    this.fields.removeAt(index);
  }

  clearTable() {
    this.fields.clear();
  }

  selecteTopic(topic: string) {
    return this.http.get(SERVER_API_URL + '/kafka-topic/' + topic, {observe: 'response'})
      .subscribe(
        res => {
          this.messageSample = res.body['message_sample'];
          this.clearTable();
          res.body['table'].forEach(e => {
            this.fields.push(this.fb.group({
              name_field: [e['name_field'], [Validators.required]],
              type: [e['type'], [Validators.required]],
              primary_key: [false, [Validators.required]],
              auto_increment: [false, [Validators.required]],
              nullable: [false, [Validators.required]],
              unique: [false, [Validators.required]],
              default: ['', [Validators.required]],
              length: [0, [Validators.required]],
              value: ['', [Validators.required]],
              collation: ['latin1_swedish_ci', [Validators.required]],
              comment: ['', [Validators.required]],
            }));
          });
        }, (error) => {
          this.showToast('An unexpected error occured', error.error, 'danger');
        }, () => {});
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

  onChangeDefault(index: number) {
    if (this.fields.at(index).get('default').value === 'USER_DEFINED') {
      (<HTMLInputElement>document.getElementById('default' + index)).style.display = 'block';
      if ((<HTMLInputElement>document.getElementById('default' + index)).value !== '') {
        this.fields.at(index).get('default').setValue(
          (<HTMLInputElement>document.getElementById('default' + index)).value);
      }
    } else {
      (<HTMLInputElement>document.getElementById('default' + index)).style.display = 'none';
    }
    // console.log(this.fields.at(index).get('default').value);
  }

  onReset(): void {
    this.streamForm.reset();
  }

  onSubmit(): void {
    const stream = this.streamForm.getRawValue();
    const res = this.http.post(SERVER_API_URL + '/stream', stream)
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.message, 'danger');
        }, () => {},
    );
  }

}
