import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ngx-streaming',
  template: `
    <router-outlet></router-outlet>
  `,
})
export class StreamingComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
