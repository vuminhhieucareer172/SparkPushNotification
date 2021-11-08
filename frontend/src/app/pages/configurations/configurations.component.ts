import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { NbToastrService } from '@nebular/theme';
import { SERVER_API_URL } from '../../app.constants';

@Component({
  selector: 'ngx-configurations',
  templateUrl: './configurations.component.html',
  styleUrls: ['./configurations.component.scss'],
})
export class ConfigurationsComponent implements OnInit {

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService
  ) { }

  ngOnInit(): void {
  }

}
