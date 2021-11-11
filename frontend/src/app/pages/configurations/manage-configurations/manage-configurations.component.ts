import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { NbGlobalPhysicalPosition, NbToastrService } from '@nebular/theme';
import { LocalDataSource } from 'ng2-smart-table';
import { SERVER_API_URL } from '../../../app.constants';

@Component({
  selector: 'ngx-manage-configurations',
  templateUrl: './manage-configurations.component.html',
  styleUrls: ['./manage-configurations.component.scss'],
})
export class ManageConfigurationsComponent implements OnInit {
  source: LocalDataSource = new LocalDataSource();
  listConfig: LocalDataSource = new LocalDataSource();
  destroyByClick = true;
  duration = 2000;
  hasIcon = true;
  preventDuplicates = false;
  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private toastrService: NbToastrService,
    private router: Router) {
    this.http.get(SERVER_API_URL + '/config')
    .subscribe(
      res => {
        this.listConfig = res as LocalDataSource;
        // console.log(res);
      }, (error) => {
        this.showToast('An unexpected error occured', error.message, 'danger');
      }, () => {},
    );
  }

  // this.http.get(SERVER_API_URL + '/config').toPromiss()
  // .then(
  //   res => {
  //     this.listConfig = res as string[];
  //   }

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

  settings = {
    hideSubHeader: true,
    actions: {
      add: false,
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
    // add: {
    //   // addButtonContent: '<i class="nb-plus"></i>',
    //   // createButtonContent: '<i class="nb-checkmark"></i>',
    //   // cancelButtonContent: '<i class="nb-close"></i>',
    // },
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
    if (window.confirm('Are you sure you want to delete this config?')) {
      this.http.delete(SERVER_API_URL + '/config/' + event.data.id).subscribe(
        res => {
          if (res['message'] == 'Successful'){
            event.confirm.resolve();
          }
        }, (error) => {
        this.showToast('An unexpected error occured', error.message, 'danger');
        }, () => {},
      );
    } else {
      event.confirm.reject();
    }
  }

}
