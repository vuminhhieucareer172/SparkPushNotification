import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { LocalDataSource } from 'ng2-smart-table';
import { environment } from '../../../../environments/environment';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-manage-queries',
  templateUrl: './manage-queries.component.html',
  styleUrls: ['./manage-queries.component.scss'],
})
export class ManageQueriesComponent implements OnInit {

  source: LocalDataSource = new LocalDataSource();
  data: Array<any>;
  destroyByClick = true;
  duration = 5000;
  hasIcon = true;
  preventDuplicates = false;

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router) {
    this.http.get(SERVER_API_URL + '/query', { observe: 'response' })
      .subscribe(
        res => {
          this.data = Object.keys(res.body).map((key) => res.body[key]);
          this.source.load(this.data);
        }, (error) => {
          this.showToast('An unexpected error occured', error.message, 'danger');
          this.data = [];
        }, () => { },
      );
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

  settings = {
    pager: {
      display: true,
      perPage: 10,
    },
    actions: {
      edit: false,
      add: false,
      delete: false,
      position: 'right',
      width: '40px',
      custom: [
        {
          name: 'edit-query',
          width: '20px',
          title: '<i class="nb-edit" title="Edit query"></i>',
        },
        {
          name: 'delete',
          width: '20px',
          title: '<i class="nb-trash" title="Delete query"></i>',
        },
      ],
    },
    columns: {
      index: {
        title: 'Index',
        type: 'number',
        width: '20px',
        valuePrepareFunction: (value, row, cell) => {
          const pager = this.source.getPaging();
          return (pager.page - 1) * pager.perPage + cell.row.index + 1;
         },
      },
      sql: {
        title: 'Sql',
        type: 'string',
      },
      topic_kafka_output: {
        title: 'Topic_kafka_output',
        type: 'string',
      },
      time_trigger: {
        title: 'Time_trigger',
        type: 'string',
      },
      created_at: {
        title: 'Created_at',
        type: 'string',
      },
      updated_at: {
        title: 'Updated_at',
        type: 'string',
      },
      contact: {
        title: 'Contact',
        type: 'string',
        valuePrepareFunction: (contact) => JSON.stringify(contact),
      },
    },
  };


  onUserRowSelect(event): void {
    this.router.navigate(['/pages/query/detail/' + event['data']['id']]);
    // console.log(event);
  }

  onCustom(event) {
    if (event.action === 'edit-query') {
      this.router.navigate(['/pages/query/detail/' + event.data.id]);
    } else if (event.action === 'delete') {
      const res = confirm(`Are you sure want to delete this config`);
      if (res) {
        this.http.delete('http://' + environment.APP_HOST + ':' + environment.APP_PORT + '/query/' + event.data.id, {observe: 'response'})
        .subscribe(
          res => {
            this.showToast('Successfull', '', 'success');
            this.http.get(SERVER_API_URL + '/query', {observe: 'response'})
              .subscribe(
                res => {
                  this.data = Object.keys(res.body).map((key) => res.body[key]);
                  this.source.load(this.data);
                },
              );
          }, (error) => {
            this.showToast('An unexpected error occured', error.error.message, 'danger');
          }, () => {},
        );
      }
    }
  }
  ngOnInit(): void {
  }

}
