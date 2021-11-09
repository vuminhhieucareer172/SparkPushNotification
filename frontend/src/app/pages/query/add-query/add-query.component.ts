import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'ngx-add-query',
  templateUrl: './add-query.component.html',
  styleUrls: ['./add-query.component.scss'],
})
export class AddQueryComponent implements OnInit {
  firstForm: FormGroup;
  secondForm: FormGroup;
  thirdForm: FormGroup;

  constructor(private fb: FormBuilder) {
  }

  ngOnInit() {
    this.firstForm = this.fb.group({
      firstCtrl: ['', Validators.required],
    });

    this.secondForm = this.fb.group({
      secondCtrl: ['', Validators.required],
    });
  }

  onFirstSubmit() {
    this.firstForm.markAsDirty();
  }

  onSecondSubmit() {
    this.secondForm.markAsDirty();
  }


}
