import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ngx-job-stream',
  template: `
    <router-outlet></router-outlet>
  `,
})
export class JobStreamComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
