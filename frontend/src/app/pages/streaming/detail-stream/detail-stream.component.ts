import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, Validators, FormArray, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NbToastrService, NbGlobalPhysicalPosition } from '@nebular/theme';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-detail-stream',
  templateUrl: './detail-stream.component.html',
  styleUrls: ['./detail-stream.component.scss'],
})
export class DetailStreamComponent implements OnInit {
  listTopicKafka: string[];
  messageSample: string;
  destroyByClick = true;
  duration = 5000;
  hasIcon = true;
  preventDuplicates = false;
  streamName: string;
  createTopic: boolean = false;

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private toastrService: NbToastrService) {
      this.route.params.subscribe(
        param => {
          this.streamName = param.streamName;
        },
      );
      this.messageSample = '';
      this.http.get(SERVER_API_URL + '/kafka-topic', {observe: 'response'})
      .subscribe(
        res => {
          this.listTopicKafka = Object.keys(res.body).map((key) => res.body[key]);
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => {},
      );
      this.http.get(SERVER_API_URL + '/stream/' + this.streamName, {observe: 'response'})
      .subscribe(
        res => {
          if (res.body['table']['collate'] === '') {
            res.body['table']['collate'] = 'latin1_swedish_ci';
          }
          this.streamForm.controls['topic_kafka_input'].setValue(res.body['topic_kafka_input']);
          this.table.controls['name'].setValue(res.body['table']['name']);
          this.table.controls['engine'].setValue(res.body['table']['engine']);
          this.table.controls['collate'].setValue(res.body['table']['collate']);
          res.body['table']['fields'].forEach(e => {
            this.fields.push(this.createFieldTable(e['name_field'], e['type'], e['primary_key'], e['auto_increment'],
              e['not_null'], e['unique'], e['default'], e['length'], e['value'], e['collation'], e['comment'],
            ));
          });
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
    fields: this.fb.array([]),
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

  onViewRecord(): void {
    this.router.navigate(['/pages/streaming/detail/' + this.streamName + '/record']);
  }

  onReset(): void {
    this.streamForm.reset();
  }

  onSubmit(): void {
    const stream = this.streamForm.getRawValue();
    this.http.put(SERVER_API_URL + '/update-stream', stream, {observe: 'response'})
      .subscribe(
        res => {
          this.showToast('Notification', 'Action completed', 'success');
          this.router.navigate(['/pages/streaming/manage-streams']);
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => {},
    );
  }
}
