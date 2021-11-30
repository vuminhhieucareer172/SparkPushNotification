import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { from } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-detail-query',
  templateUrl: './detail-query.component.html',
  styleUrls: ['./detail-query.component.scss']
})
export class DetailQueryComponent implements OnInit {
  input_check = '';
  destroyByClick = true;
  duration = 2000;
  hasIcon = true;
  preventDuplicates = false;
  schedule: string;
  listTableQuery = [];
  listQueryField = [];
  listTopicKafka = [];
  topicValid = false;
  methodSelected = '';
  isValidEmail = true;
  isValidTele = true;
  queryId: string;

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router,
    private route: ActivatedRoute,) {
    this.route.params.subscribe(
      param => {
        this.queryId = param.queryId;
      },
    );
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

    // for (const stream of this.listTableQuery) {
    //   console.log('av');
    // }
    // this.http.get(SERVER_API_URL + '/stream/' + 'dbstreaming_streaming_jobetl', { observe: 'response' })
    //   .subscribe(
    //     res => {
    //       // for (const name_field of res.body['table']['fields']) {
    //       //   this.listQueryField.push(stream + '.' + name_field['name_field']);
    //       // }
    //       console.log(res);
    //     }, (error) => {
    //       this.showToast('An unexpected error occured', error.error.message, 'warning');
    //     }, () => { });
    // }

    this.http.get(SERVER_API_URL + '/kafka-topic', { observe: 'response' })
      .subscribe(
        res => {
          for (const topic of Object(res.body)) {
            this.listTopicKafka.push(topic);
          }
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => { },
      );
    this.http.get(SERVER_API_URL + '/query/' + this.queryId, { observe: 'response' })
      .subscribe(
        res => {
          console.log(res);
          this.manualInputForm.controls['manualText'].setValue(res.body['sql']);
          this.scheduleAndContactForm.controls['topicOutput'].setValue(res.body['topic_kafka_output']);
          this.scheduleAndContactForm.controls['selectMethod'].setValue(res.body['contact']['method']);
          this.scheduleAndContactForm.controls['inputMethod'].setValue(res.body['contact']['value']);
          if (res.body['time_trigger'] < (60 * 60) && ((res.body['time_trigger'] % 60) == 0)) {
            this.scheduleAndContactForm.controls['selectSchedule'].setValue('minute');
            this.scheduleAndContactForm.controls['inputTime'].setValue(res.body['time_trigger'] / 60);
          } else if (res.body['time_trigger'] < (60 * 60 * 24) && ((res.body['time_trigger'] % 3600) == 0)) {
            this.scheduleAndContactForm.controls['selectSchedule'].setValue('hour');
            this.scheduleAndContactForm.controls['inputTime'].setValue(res.body['time_trigger'] / 3600);
          } else if (res.body['time_trigger'] >= (60 * 60 * 24) && ((res.body['time_trigger'] % (60 * 60 * 24)) == 0)) {
            this.scheduleAndContactForm.controls['selectSchedule'].setValue('day');
            this.scheduleAndContactForm.controls['inputTime'].setValue(res.body['time_trigger'] / (60 * 60 * 24));
          }

          // push vao from =========================================
          if (res.body['sql'].split('select')[1].split('from')[1].includes('where')) {
            var fromTable = [];
            if (res.body['sql'].split('select')[1].split('from')[1].split('where')[0].includes(',')) {
              for (const table of res.body['sql'].split('select')[1].split('from')[1].split('where')[0].split(',')) {
                fromTable.push({ 'tableQuery': table.trim() });
              }
              fromTable.forEach(e => {
                this.fieldsTableQuery.push(this.createFieldTableQuery(e['tableQuery']));
              });
            } else {
              fromTable.push({ 'tableQuery': res.body['sql'].split('select')[1].split('from')[1].split('where')[0].trim() });
              fromTable.forEach(e => {
                this.fieldsTableQuery.push(this.createFieldTableQuery(e['tableQuery']));
              });
            }
          } else {
            var fromTable = [];
            fromTable.push({ 'tableQuery': res.body['sql'].split('select')[1].split('from')[1].trim() });
            fromTable.forEach(e => {
              this.fieldsTableQuery.push(this.createFieldTableQuery(e['tableQuery']));
            });
          }
          // push vao from =========================================

          // push vao select =========================================
          if (res.body['sql'].split('select')[1].split('from')[0].includes(',')) {
            const selectArr = [];
            for (let selectColumn of res.body['sql'].split('select')[1].split('from')[0].split(',')) {
              selectArr.push({ 'queryField': selectColumn.trim() });
            }
            // console.log(selectArr);

            selectArr.forEach(e => {
              // console.log(e);
              this.fieldsQueryField.push(this.createFieldQueryField(e['queryField']));
            });
          } else {
            // console.log(res.body['sql'].split('select')[1].split('from'));
            this.fieldsQueryField.push(this.createFieldQueryField(res.body['sql'].split('select')[1].split('from')[0]));
          }
          // push vao select =========================================

          // push vao where =========================================
          // if (res.body['sql'].split('select')[1].split('from')[1].includes('where')) {
          //   var fromTable = [];
          //   if (res.body['sql'].split('select')[1].split('from')[1].split('where')[0].includes(',')) {
          //     for (const table of res.body['sql'].split('select')[1].split('from')[1].split('where')[0].split(',')) {
          //       fromTable.push({ 'tableQuery': table.trim() });
          //     }
          //     fromTable.forEach(e => {
          //       this.fieldsTableQuery.push(this.createFieldTableQuery(e['tableQuery']));
          //     });
          //   } else {
          //     fromTable.push({ 'tableQuery': res.body['sql'].split('select')[1].split('from')[1].split('where')[0].trim() });
          //     fromTable.forEach(e => {
          //       this.fieldsTableQuery.push(this.createFieldTableQuery(e['tableQuery']));
          //     });
          //   }
          // } else {
          //   var fromTable = [];
          //   fromTable.push({ 'tableQuery': res.body['sql'].split('select')[1].split('from')[1].trim() });
          //   fromTable.forEach(e => {
          //     this.fieldsTableQuery.push(this.createFieldTableQuery(e['tableQuery']));
          //   });
          // }

          // push vao where =========================================

        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'danger');
        }, () => { },
      );
  }

  ngOnInit(): void {
    console.log('a');
    for (const stream of this.listTableQuery) {
      console.log('av');
      this.http.get(SERVER_API_URL + '/stream/' + stream, { observe: 'response' })
      .subscribe(
        res => {
          for (const name_field of res.body['table']['fields']) {
            this.listQueryField.push(stream + '.' + name_field['name_field']);
          }
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'warning');
        }, () => { });
    }
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

  onSelectSchedule(value: string): void {
    this.schedule = value;
    if (this.schedule === 'manual-input') {
      // this.quickInputForm.reset();
    } else if (this.schedule === 'quick-input') {
      // this.manualInputForm.reset();
    }
  }

  manualInputForm = this.fb.group({
    manualText: ['', [Validators.required, this.isSelectQuery]],
  });

  isSelectQuery(control: FormControl): { [key: string]: boolean } | null {
    if (control.value == null) {
      return { validMaster: true };
    } else if (!control.value.toLowerCase().startsWith('select')) {
      return { validMaster: true };
    }
    return null;
  }

  onSubmitManual(): void {
    const manualValue = this.manualInputForm.getRawValue();
  }

  createFieldTableQuery(tableQuery: string = null): FormGroup {
    return this.fb.group({
      tableQuery: [tableQuery, []],
    });
  }

  createFieldQueryField(queryField: string = null): FormGroup {
    // console.log(this.fb.group({
    //   queryField: [queryField, []],
    // }));
    return this.fb.group({
      queryField: [queryField, []],
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

  createFieldHavingConditions(method: string = null, field: string = null, operator: string = null, value: string = null): FormGroup {
    return this.fb.group({
      method: [method, [Validators.required]],
      field: [field, [Validators.required]],
      operator: [operator, [Validators.required]],
      value: [value, [Validators.required]],
    });
  }

  createOrder(orderField: string = null, order: string = null): FormGroup {
    return this.fb.group({
      orderField: [orderField, [Validators.required]],
      order: [orderField, [Validators.required]],
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
    this.http.get(SERVER_API_URL + '/stream/' + stream, { observe: 'response' })
      .subscribe(
        res => {
          for (const name_field of res.body['table']['fields']) {
            this.listQueryField.push(stream + '.' + name_field['name_field']);
          }
        }, (error) => {
          this.showToast('An unexpected error occured', error.error.message, 'warning');
        }, () => { });
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
    // console.log(quickValue)
  }

  scheduleAndContactForm = this.fb.group({
    topicOutput: ['', [Validators.required]],
    selectSchedule: ['minute', [Validators.required]],
    inputTime: ['', [Validators.required, Validators.pattern('^[0-9]*$')]],
    selectMethod: ['', [Validators.required]],
    inputMethod: ['', [Validators.required]],
    // inputMethodTelegram: ['', [Validators.pattern('^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$')]],
  });

  isValidTopic(inputValue): void {
    if (this.listTopicKafka.includes(inputValue)) {
      this.topicValid = true;
    } else {
      this.topicValid = false;
    }
  }

  isValidRegex(inputValue): void {
    const emailRegex = new RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
    const teleRegex = new RegExp(/^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$/);
    if (this.methodSelected === 'email') {
      if (emailRegex.test(inputValue)) {
        this.isValidEmail = emailRegex.test(inputValue);
      } else {
        this.isValidEmail = false;
      }
    } else if (this.methodSelected === 'telegram') {
      if (teleRegex.test(inputValue)) {
        this.isValidTele = teleRegex.test(inputValue);
      } else {
        this.isValidTele = false;
      }
    }
    // console.log('scheduleAndContactForm ' + !this.scheduleAndContactForm.valid);
    // console.log('manualInputForm ' + !this.manualInputForm.valid);
    // console.log('isValidEmail ' + !this.isValidEmail);
    // console.log('tong hop form' + ((!this.scheduleAndContactForm.valid || !this.manualInputForm.valid) || !this.isValidEmail));
    // console.log('quickInputForm ' + !this.quickInputForm.valid);
    // console.log('tong hop quick ' + (!this.scheduleAndContactForm.valid || !this.quickInputForm.valid));

    // console.log('-------/-');

    // console.log(((!this.scheduleAndContactForm.valid || !this.manualInputForm.valid) || !this.isValidEmail) && (!this.scheduleAndContactForm.valid || !this.quickInputForm.valid));

  }

  onScheduleAndContact(): void {
    const quickValue1 = this.scheduleAndContactForm.getRawValue();
    const quickValue2 = this.quickInputForm.getRawValue();
    const quickValue3 = this.manualInputForm.getRawValue();
  }

  onSubmitAll(): void {
    if (this.schedule === 'manual-input') {
      const scheduleAndContact = this.scheduleAndContactForm.getRawValue();
      const manualInput = this.manualInputForm.getRawValue();
      const json_result = {};
      const contact = {};
      // console.log(scheduleAndContact);
      if (manualInput.manualText.toLowerCase().includes('from')) {
        json_result['sql'] = manualInput.manualText;
      }
      json_result['topic_kafka_output'] = scheduleAndContact.topicOutput;
      if (scheduleAndContact.selectSchedule === 'minute') {
        json_result['time_trigger'] = scheduleAndContact.inputTime * 60;
      } else if (scheduleAndContact.selectSchedule === 'hour') {
        json_result['time_trigger'] = scheduleAndContact.inputTime * 60 * 60;
      } else if (scheduleAndContact.selectSchedule === 'day') {
        json_result['time_trigger'] = scheduleAndContact.inputTime * 60 * 60 * 24;
      }

      contact['method'] = scheduleAndContact.selectMethod;
      contact['value'] = scheduleAndContact.inputMethod;
      json_result['contact'] = contact;
      this.http.post(SERVER_API_URL + '/kafka-topic/create', { 'topic_name': scheduleAndContact.topicOutput }, { observe: 'response' })
        .subscribe(
          res => {
            this.showToast('Notification', 'Added new topic kafka', 'success');
          }, (error) => {
            this.showToast('An unexpected error occured', error.error.message, 'danger');
          }, () => { });
      this.http.put('http://' + environment.APP_HOST + ':' + environment.APP_PORT_SCHEDULER + '/query', json_result, { observe: 'response' })
        .subscribe(
          res => {
            this.showToast('Notification', 'Action completed', 'success');
            this.scheduleAndContactForm.reset();
            this.manualInputForm.reset();
          }, (error) => {
            this.showToast('An unexpected error occured', error.error.message, 'danger');
          }, () => { },
        );
    } else if (this.schedule === 'quick-input') {
      let finalSQL = 'select ';
      const json_result = {};
      const contact = {};
      const scheduleAndContact = this.scheduleAndContactForm.getRawValue();
      const quickInput = this.quickInputForm.getRawValue();

      let lenQueryField = quickInput.fieldsQueryField.length;
      for (const queryField of quickInput.fieldsQueryField) {
        if (lenQueryField >= 2) {
          finalSQL += queryField['queryField'] + ', ';
          lenQueryField -= 1;
        } else if (lenQueryField < 2) {
          finalSQL += queryField['queryField'] + ' ';
        }
      }
      finalSQL += 'from ';
      let lenTableQuery = quickInput.fieldsTableQuery.length;
      for (const tableQuery of quickInput.fieldsTableQuery) {
        if (lenTableQuery >= 2) {
          finalSQL += tableQuery['tableQuery'] + ', ';
          lenTableQuery -= 1;
        } else if (lenTableQuery < 2) {
          finalSQL += tableQuery['tableQuery'] + ' ';
        }
      }
      let lenConditions = quickInput.fieldsConditions.length;
      if (lenConditions > 0) {
        finalSQL += 'where ';
        for (const condition of quickInput.fieldsConditions) {
          if (lenConditions >= 2) {
            finalSQL += condition['field'] + ' ' + condition['operator'] + ' ' + condition['value'] + ' ' + 'and ';
            lenConditions -= 1;
          } else if (lenConditions < 2) {
            finalSQL += condition['field'] + ' ' + condition['operator'] + ' ' + condition['value'] + ' ';
          }
        }
      }
      let lenGroup = quickInput.fieldsGroup.length;
      if (lenGroup > 0) {
        finalSQL += 'group by ';
        for (const group of quickInput.fieldsGroup) {
          if (lenGroup >= 2) {
            finalSQL += group['groupField'] + ', ';
            lenGroup -= 1;
          } else if (lenGroup < 2) {
            finalSQL += group['groupField'] + ' ';
          }
        }
      }
      let lenHavingConditions = quickInput.fieldsHavingConditions.length;
      if (lenHavingConditions > 0) {
        finalSQL += 'having ';
        for (const havingCondition of quickInput.fieldsHavingConditions) {
          if (lenHavingConditions >= 2) {
            finalSQL += havingCondition['method'] + '(' + havingCondition['field'] + ')' + ' ' + havingCondition['operator'] + ' ' + havingCondition['value'] + ' ' + 'and ';
            lenHavingConditions -= 1;
          } else if (lenHavingConditions < 2) {
            finalSQL += havingCondition['method'] + '(' + havingCondition['field'] + ')' + ' ' + havingCondition['operator'] + ' ' + havingCondition['value'] + ' ';
          }
        }
      }
      let lenOrder = quickInput.fieldsOrder.length;
      if (lenOrder > 0) {
        finalSQL += 'order by ';
        for (const fieldOrder of quickInput.fieldsOrder) {
          if (lenOrder >= 2) {
            finalSQL += fieldOrder['orderField'] + ' ' + fieldOrder['order'] + ', ';
            lenOrder -= 1;
          } else if (lenOrder < 2) {
            finalSQL += fieldOrder['orderField'] + ' ' + fieldOrder['order'];
          }
        }
      }
      finalSQL += ';';
      json_result['sql'] = finalSQL;
      json_result['topic_kafka_output'] = scheduleAndContact.topicOutput;
      if (scheduleAndContact.selectSchedule === 'minute') {
        json_result['time_trigger'] = scheduleAndContact.inputTime * 60;
      } else if (scheduleAndContact.selectSchedule === 'hour') {
        json_result['time_trigger'] = scheduleAndContact.inputTime * 60 * 60;
      } else if (scheduleAndContact.selectSchedule === 'day') {
        json_result['time_trigger'] = scheduleAndContact.inputTime * 60 * 60 * 24;
      }

      contact['method'] = scheduleAndContact.selectMethod;
      contact['value'] = scheduleAndContact.inputMethod;
      json_result['contact'] = contact;
      this.http.post(SERVER_API_URL + '/kafka-topic/create', { 'topic_name': scheduleAndContact.topicOutput }, { observe: 'response' })
        .subscribe(
          res => {
            this.showToast('Notification', 'Added new topic kafka', 'success');
          }, (error) => {
            this.showToast('An unexpected error occured', error.error.message, 'danger');
          }, () => { });
      this.http.put('http://' + environment.APP_HOST + ':' + environment.APP_PORT_SCHEDULER + '/query', json_result, { observe: 'response' })
        .subscribe(
          res => {
            this.showToast('Notification', 'Action completed', 'success');
            this.scheduleAndContactForm.reset();
            this.manualInputForm.reset();
          }, (error) => {
            this.showToast('An unexpected error occured', error.error.message, 'danger');
          }, () => { },
        );
      // console.log(finalSQL)
    }
  }

  selectedMethod(selected: string): void {
    this.methodSelected = selected;
  }

  onSelectInputCheck(value: string): void {
    this.input_check = value;
  }

}
