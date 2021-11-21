import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl, FormArray } from '@angular/forms';
import {  NbToastrService } from '@nebular/theme';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'ngx-add-query',
  templateUrl: './add-query.component.html',
  styleUrls: ['./add-query.component.scss'],
})
export class AddQueryComponent  implements OnInit, OnDestroy {
  firstForm: FormGroup;
  secondForm: FormGroup;
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

  private alive: boolean;
  objectKeys = Object.keys;

  jobForm = this.fb.group({
    name_job: ['', (Validators.required)],
    schedule: ['', [Validators.required]],
  });

  table = this.fb.group({
    name: new FormControl('', (Validators.required)),
    charset: ['', [Validators.required]],
    collate: ['', [Validators.required]],
    engine: ['InnoDB', [Validators.required]],
    fields: this.fb.array([this.createFieldTable()]),
  });

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

  // manualForm = this.fb.group({
  //   manualText: ['', [Validators.required]],
  // });

  ngOnInit() {
    this.firstForm = this.fb.group({});
    this.secondForm = this.fb.group({});
  }

  onFirstSubmit() {
    this.firstForm.markAsDirty();
  }

  onSecondSubmit() {
    this.secondForm.markAsDirty();
  }

  onSelectSchedule(value: string): void {
    this.schedule = value;
  }

  setSchedule(value: string): void {
    this.jobForm.controls['schedule'].setValue(value);
  }

  ngOnDestroy(): void {
    this.alive = false;
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

}
