import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { NbToastrService } from '@nebular/theme';
import { LocalDataSource } from 'ng2-smart-table';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-manage-configurations',
  templateUrl: './manage-configurations.component.html',
  styleUrls: ['./manage-configurations.component.scss'],
})
export class ManageConfigurationsComponent implements OnInit {
  source: LocalDataSource = new LocalDataSource();
  listConfig: string[];
  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router) {
    this.http.get(SERVER_API_URL + '/config').toPromise().then(
      res => {
        this.listConfig = res as string[];
      },
    );
  }

  ngOnInit(): void {
  }

  settings = {
    actions: {
      position: 'right',
    },
    columns: {
      id: {
        title: 'ID',
        type: 'number',
      },
      name: {
        title: 'Name',
        type: 'string',
      },
      value: {
        title: 'Value',
        valuePrepareFunction: (value) => JSON.stringify(value),
      },
    },
    add: {
      addButtonContent: '<i class="nb-plus"></i>',
      createButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
    },
    edit: {
      editButtonContent: '<i class="nb-edit"></i>',
      saveButtonContent: '<i class="nb-checkmark"></i>',
      cancelButtonContent: '<i class="nb-close"></i>',
    },
    delete: {
      deleteButtonContent: '<i class="nb-trash"></i>',
      confirmDelete: true,
    },
  };

  onDeleteConfirm(event): void {
    // console.log(event['data']['table_name']);
    this.router.navigate([event['data']['table_name']]);
  }

}
