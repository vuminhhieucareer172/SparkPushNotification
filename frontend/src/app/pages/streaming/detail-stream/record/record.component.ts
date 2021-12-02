import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NbToastrService, NbGlobalPhysicalPosition } from '@nebular/theme';
import { LocalDataSource } from 'ng2-smart-table';
import { SERVER_API_URL } from '../../../../app.constants';

@Component({
  selector: 'ngx-record',
  templateUrl: './record.component.html',
  styleUrls: ['./record.component.scss'],
})
export class RecordComponent implements OnInit {
  data: Array<any>;
  source: LocalDataSource = new LocalDataSource();
  destroyByClick = true;
  duration = 5000;
  hasIcon = true;
  preventDuplicates = false;
  streamName: string;
  settings: {[k: string]: any} = {};

  constructor(
    private router: Router,
    private http: HttpClient,
    private route: ActivatedRoute,
    private toastrService: NbToastrService) {
      this.route.params.subscribe(
        param => {
          this.streamName = param.streamName;
        },
      );
      this.settings.actions = {
        edit: false,
        add: false,
        delete: false,
      };
      this.settings.pager = {
        display: true,
        perPage: 10,
        };
      this.settings.columns = {};
      this.http.get(SERVER_API_URL + '/stream/record/' + this.streamName, {observe: 'response'})
        .subscribe(
          res => {
            if (Object.keys(res.body).length) {
              Object.keys(res.body[0]).forEach((key) => {
                this.settings.columns[key] = {
                  title: key,
                  type: typeof res.body[0][key],
                };
              });
              const newSettings = this.settings;
              this.settings = Object.assign({}, newSettings );
              this.data = Object.keys(res.body).map((key) => res.body[key]);
              this.source.load(this.data);
            }
          }, (error) => {
            this.showToast('An unexpected error occurred', error.error.message, 'danger');
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

}
