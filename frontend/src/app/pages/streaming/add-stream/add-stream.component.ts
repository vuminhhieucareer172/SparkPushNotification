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
  duration = 5000;
  hasIcon = true;
  preventDuplicates = false;
  createTopic: boolean = false;

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService) {
    this.messageSample = '';
    this.http.get(SERVER_API_URL + '/kafka-topic', {observe: 'response'})
    .subscribe(
      res => {
        this.listTopicKafka = Object.keys(res.body).map((key) => res.body[key]);
        // console.log(this.listTopicKafka)
      }, (error) => {
        this.showToast('An unexpected error occured', error.error.message, 'danger');
      }, () => {},
    );
  }

  table = this.fb.group({
    name: new FormControl('', (Validators.required)),
    charset: ['', [Validators.required]],
    collate: ['latin1_swedish_ci', [Validators.required]],
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

  createFieldTable(nameField: string = null, type: string = null, primaryKey: boolean = false, autoIncrement: boolean = false,
                    notNull: boolean = false, unique: boolean = false, defaultValue: string = null,
                    length: number = 0, value: string = '', collation: string = null, comment: string = null): FormGroup {
    return this.fb.group({
      name_field: [nameField, [Validators.required]],
      type: [type, [Validators.required]],
      primary_key: [primaryKey, [Validators.required]],
      auto_increment: [autoIncrement, [Validators.required]],
      not_null: [notNull, [Validators.required]],
      unique: [unique, [Validators.required]],
      default: [defaultValue, [Validators.required]],
      length: [length, [Validators.required]],
      value: [value, [Validators.required]],
      collation: [collation, []],
      comment: [comment, [Validators.required]],
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

  onCreateTopic(topic: string): void {
    this.http.post(SERVER_API_URL + '/kafka-topic/create', {'topic_name': topic}, {observe: 'response'})
      .subscribe(
        res => {
          this.listTopicKafka.push(topic);
          this.showToast('Notification', 'Added new topic kafka', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => {});
  }

  selecteTopic(topic: string): void {
    this.http.get(SERVER_API_URL + '/kafka-topic/' + topic, {observe: 'response'})
      .subscribe(
        res => {
          this.messageSample = res.body['message_sample'];
          this.clearTable();
          res.body['table'].forEach(e => {
            this.fields.push(this.createFieldTable(e['name_field'], e['type']));
          });
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'warning');
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

  onReset(): void {
    this.streamForm.reset();
  }

  onSubmit(): void {
    const stream = this.streamForm.getRawValue();
    this.http.post(SERVER_API_URL + '/add-stream', stream, {observe: 'response'})
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => {},
    );
  }

}
