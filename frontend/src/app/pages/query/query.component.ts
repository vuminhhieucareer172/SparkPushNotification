import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ngx-query',
  template: `
  <router-outlet></router-outlet>
  `,
})
export class QueryComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
