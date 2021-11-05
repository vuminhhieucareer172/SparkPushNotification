import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'ngx-manage',
  templateUrl: './manage.component.html',
  styleUrls: ['./manage.component.scss'],
})
export class ManageComponent implements OnInit {
  hours: any[];
  minutes: number[];
  seconds: number[];
  days: any[];
  schedule: string;

  constructor() {
    this.minutes = Array.from(Array(60), (_, i) => i);
    this.seconds = Array.from(Array(60), (_, i) => i);
    this.hours = Array.from(Array(24), (_, i) => i);
    this.days = Array.from(Array(30), (_, i) => i);
  }

  ngOnInit(): void {
  }

  onSelect(value: string): void {
    this.schedule = value;
  }
}
