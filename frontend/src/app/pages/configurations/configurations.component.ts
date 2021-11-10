import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { SERVER_API_URL } from '../../app.constants';
import { LocalDataSource } from 'ng2-smart-table';
import { SmartTableData } from '../../@core/data/smart-table';
import { Router } from '@angular/router';
import { type } from 'os';


@Component({
  selector: 'ngx-configurations',
  template: `
  <router-outlet></router-outlet>
  `,
  // styleUrls: ['./configurations.component.scss'],
  // templateUrl: './configurations.component.html',
})
export class ConfigurationsComponent implements OnInit {
  constructor() { }

  ngOnInit(): void {
  }

}
