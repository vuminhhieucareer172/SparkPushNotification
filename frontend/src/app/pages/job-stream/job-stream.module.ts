import { NgModule } from '@angular/core';
import {
  NbButtonModule,
  NbCardModule,
  NbTabsetModule,
  NbUserModule,
  NbIconModule,
  NbSelectModule,
  NbListModule,
  NbInputModule,
  NbCheckboxModule,
  NbRadioModule,
} from '@nebular/theme';
import { ChartModule } from 'angular2-chartjs';
import { JobStreamComponent } from './job-stream.component';
import { CommonModule } from '@angular/common';
import { ManageComponent } from './manage/manage.component';
import { JobStreamRoutingModule } from './job-stream-routing.module';
import { ReactiveFormsModule } from '@angular/forms';
import { CronJobsModule } from 'ngx-cron-jobs';

@NgModule({
  imports: [
    CommonModule,
    JobStreamRoutingModule,
    NbCardModule,
    NbUserModule,
    NbButtonModule,
    NbIconModule,
    NbInputModule,
    NbTabsetModule,
    NbSelectModule,
    NbListModule,
    ChartModule,
    NbCheckboxModule,
    NbRadioModule,
    ReactiveFormsModule,
    CronJobsModule,
  ],
  declarations: [
    JobStreamComponent,
    ManageComponent,
  ],
})
export class JobStreamModule { }
