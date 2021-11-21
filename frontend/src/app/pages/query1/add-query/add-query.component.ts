import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-add-query',
  templateUrl: './add-query.component.html',
  styleUrls: ['./add-query.component.scss'],
})
export class AddQueryComponent implements OnInit {
  input_check = '';
  destroyByClick = true;
  duration = 2000;
  hasIcon = true;
  preventDuplicates = false;
  schedule: string;
  listTableQuery = [];
  listQueryField = [];

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router) {
    this.http.get(SERVER_API_URL + '/stream', { observe: 'response' })
      .subscribe(
        res => {
          for (const table of Object(res.body)) {
            this.listTableQuery.push(table['table_name']);
          }
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => { },
      );
  }

  ngOnInit(): void {
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


  disableOrNot() {
    // if (this.input_check == 'quick_input') {
    //   return true
    // }
    // if (this.input_check == 'manual_input') {
    //   return false
    // }
    if (this.input_check == '') {
      return true
    }
  }

  onSelectSchedule(value: string): void {
    this.schedule = value;
  }

  manualInputForm = this.fb.group({
    manualText: ['', [Validators.required]],
  });

  onSubmitManual(): void {
    const manualValue = this.manualInputForm.getRawValue();
    console.log(manualValue)
  }

  createFieldTableQuery(tableQuery: string = null): FormGroup {
    return this.fb.group({
      tableQuery: [tableQuery, [Validators.required]],
    });
  }

  createFieldQueryField(queryField: string = null): FormGroup {
    return this.fb.group({
      queryField: [queryField, [Validators.required]],
    });
  }

  createFieldConditions(field: string = null, operator: string = null, value: string = null): FormGroup {
    return this.fb.group({
      field: [field, [Validators.required]],
      operator: [operator, [Validators.required]],
      value: [value, [Validators.required]],
    });
  }

  createGroup(groupField: string = null): FormGroup {
    return this.fb.group({
      groupField: [groupField, [Validators.required]],
    });
  }

  createFieldHavingConditions(field: string = null, operator: string = null, value: string = null): FormGroup {
    return this.fb.group({
      field: [field, [Validators.required]],
      operator: [operator, [Validators.required]],
      value: [value, [Validators.required]],
    });
  }

  createOrder(orderField: string = null): FormGroup {
    return this.fb.group({
      orderField: [orderField, [Validators.required]],
    });
  }

  quickInputForm = this.fb.group({
    fieldsTableQuery: this.fb.array([]),
    fieldsQueryField: this.fb.array([]),
    fieldsConditions: this.fb.array([]),
    fieldsGroup: this.fb.array([]),
    fieldsHavingConditions: this.fb.array([]),
    fieldsOrder: this.fb.array([]),
  });

  selecteTableStream(stream: string): void {
    this.http.get(SERVER_API_URL + '/stream/' + stream, {observe: 'response'})
      .subscribe(
        res => {
          for (const name_field of res.body['table']['fields']) {
            this.listQueryField.push(stream + '.' + name_field['name_field']);
          }
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'warning');
        }, () => {});
  }

  get fieldsTableQuery(): FormArray {
    return <FormArray>this.quickInputForm.get('fieldsTableQuery');
  }

  get fieldsQueryField(): FormArray {
    return <FormArray>this.quickInputForm.get('fieldsQueryField');
  }

  get fieldsConditions(): FormArray {
    return <FormArray>this.quickInputForm.get('fieldsConditions');
  }

  get fieldsGroup(): FormArray {
    return <FormArray>this.quickInputForm.get('fieldsGroup');
  }

  get fieldsHavingConditions(): FormArray {
    return <FormArray>this.quickInputForm.get('fieldsHavingConditions');
  }

  get fieldsOrder(): FormArray {
    return <FormArray>this.quickInputForm.get('fieldsOrder');
  }

  addTableQuery() {
    this.fieldsTableQuery.push(this.createFieldTableQuery());
  }

  addQueryField() {
    this.fieldsQueryField.push(this.createFieldQueryField());
  }

  addConditions() {
    this.fieldsConditions.push(this.createFieldConditions());
  }

  addGroup() {
    this.fieldsGroup.push(this.createGroup());
  }

  addHavingConditions() {
    this.fieldsHavingConditions.push(this.createFieldHavingConditions());
  }

  addOrder() {
    this.fieldsOrder.push(this.createOrder());
  }

  dropTableQuery(index: number) {
    this.fieldsTableQuery.removeAt(index);
  }

  dropQueryField(index: number) {
    this.fieldsQueryField.removeAt(index);
  }

  dropConditions(index: number) {
    this.fieldsConditions.removeAt(index);
  }

  dropGroup(index: number) {
    this.fieldsGroup.removeAt(index);
  }

  dropHavingConditions(index: number) {
    this.fieldsHavingConditions.removeAt(index);
  }

  dropOrder(index: number) {
    this.fieldsOrder.removeAt(index);
  }

  onSubmitQuick(): void {
    const quickValue = this.quickInputForm.getRawValue();
    console.log(quickValue)
  }

  scheduleAndContact = this.fb.group({
    // manualText: ['', [Validators.required]],
  });

  onScheduleAndContact(): void {
    const quickValue = this.scheduleAndContact.getRawValue();
    console.log(quickValue)
  }

  onSelectInputCheck(value: string): void {
    this.input_check = value;
  }

}
