import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { LocalDataSource } from 'ng2-smart-table';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-manage-streams',
  templateUrl: './manage-streams.component.html',
  styleUrls: ['./manage-streams.component.scss'],
})
export class ManageStreamsComponent implements OnInit {
  data: Array<any>;
  source: LocalDataSource = new LocalDataSource();
  destroyByClick = true;
  duration = 5000;
  hasIcon = true;
  preventDuplicates = false;

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
      custom: [
        {
          name: 'view-record',
          title: '<i class="ion-forward" title="View record"></i>',
        },
        {
          name: 'delete',
          title: '<i class="nb-trash" title="Delete stream"></i>',
        },
      ],
    } ,
    columns: {
      index: {
        title: '#',
        type: 'number',
        width: '20px',
        valuePrepareFunction: (value, row, cell) => {
          const pager = this.source.getPaging();
          return (pager.page - 1) * pager.perPage + cell.row.index + 1;
         },
      },
      table_name: {
        title: 'Table name',
        type: 'string',
      },
      topic_kafka: {
        title: 'Topic Kafka',
        type: 'string',
      },
    },
  };

  constructor(
    private router: Router,
    private http: HttpClient,
    private toastrService: NbToastrService) {
    this.http.get(SERVER_API_URL + '/stream', {observe: 'response'})
      .subscribe(
        res => {
          this.data = Object.keys(res.body).map((key) => res.body[key]);
          this.source.load(this.data);
        }, (error) => {
          this.showToast('An unexpected error occured', error.message, 'danger');
          this.data = [];
        }, () => {},
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

  onUserRowSelect(event): void {
    this.router.navigate(['/pages/streaming/detail/' + event['data']['table_name']]);
  }

  onCustom(event) {
    if (event.action === 'view-record') {
      this.router.navigate(['/pages/streaming/detail/' + event.data.table_name + '/record']);
    } else if (event.action === 'delete') {
      const res = confirm(`Are you sure want to delete this stream, table streaming also has been dropped?`);
      if (res) {
        this.http.delete(SERVER_API_URL + '/stream/' + event.data.table_name, {observe: 'response'})
        .subscribe(
          res => {
            this.showToast('Successfull', '', 'success');
            this.http.get(SERVER_API_URL + '/stream', {observe: 'response'})
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

}
