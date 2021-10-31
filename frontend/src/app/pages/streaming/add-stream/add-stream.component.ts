import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, Validators, FormGroup, FormArray, FormControl } from '@angular/forms';
import { SERVER_API_URL } from '../../../app.constants';
import { DOCUMENT } from '@angular/common'; 

@Component({
  selector: 'ngx-add-stream',
  templateUrl: './add-stream.component.html',
  styleUrls: ['./add-stream.component.scss'],
})
export class AddStreamComponent implements OnInit {
  constructor(
    private http: HttpClient,
    private fb: FormBuilder) {
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

  get fields():FormArray{
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

  onChangeDefault(index: number) {
    if (this.fields.at(index).get('default').value == 'USER_DEFINED') {
      (<HTMLInputElement>document.getElementById('default' + index)).style.display = 'block';
      if ((<HTMLInputElement>document.getElementById('default' + index)).value != '') {
        this.fields.at(index).get('default').setValue((<HTMLInputElement>document.getElementById('default' + index)).value);
      }
    } else {
      (<HTMLInputElement>document.getElementById('default' + index)).style.display = 'none';
    }
    console.log(this.fields.at(index).get('default').value);
  }

  onSubmit(): void {
    const stream = this.streamForm.getRawValue();
    console.log(stream);

    const res = this.http.post(SERVER_API_URL + '/stream', stream).subscribe(
      res => {
        console.log(res);
      },
    );
  }

}
