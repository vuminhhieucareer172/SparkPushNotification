import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { NbToastrService } from '@nebular/theme';
import { SERVER_API_URL } from '../../app.constants';
import { LocalDataSource } from 'ng2-smart-table';
import { SmartTableData } from '../../@core/data/smart-table';
import { Router } from '@angular/router';


@Component({
  selector: 'ngx-configurations',
  styleUrls: ['./configurations.component.scss'],
  templateUrl: './configurations.component.html',
})
export class ConfigurationsComponent implements OnInit {

  source: LocalDataSource = new LocalDataSource();

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router,
  ) {
      // const data = this.http.get(SERVER_API_URL + '/config');
      // this.source.load(data);
   }

  ngOnInit(): void {
  }

  kafkaForm = this.fb.group({
  });

  sparkForm = this.fb.group({
  });

  emailForm = this.fb.group({
  });

  onSubmitKafka(): void {
  }

  onSubmitSpark(): void {
  }

  onSubmitEmail(): void {
  }

  settings = {
    actions: {
      position: 'right',
    } ,
    columns: {
      id: {
        title: 'ID',
        type: 'number',
      },
      firstName: {
        title: 'Name',
        type: 'string',
      },
      lastName: {
        title: 'Value',
        type: 'string',
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
    console.log(event['data']['table_name']);
    this.router.navigate([event['data']['table_name']]);
  }

  // onDeleteConfirm(event): void {
  //   if (window.confirm('Are you sure you want to delete?')) {
  //     event.confirm.resolve();
  //   } else {
  //     event.confirm.reject();
  //   }
  // }

}
