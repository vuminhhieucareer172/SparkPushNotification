import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'ngx-manage-streams',
  templateUrl: './manage-streams.component.html',
  styleUrls: ['./manage-streams.component.scss'],
})
export class ManageStreamsComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  settings = {
    actions: { 
      position: 'right'
    } ,
    columns: {
      index: {
        title: '#',
        type: 'number',
        width: '20px'
      },
      table_name: {
        title: 'Table Name',
        type: 'string',
      },
      topic_kafka_input: {
        title: 'Topic kafka input',
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
  onUserRowSelect(event): void {
    console.log(event['data']['table_name']);
    this.router.navigate([event['data']['table_name']]);
  }

}
