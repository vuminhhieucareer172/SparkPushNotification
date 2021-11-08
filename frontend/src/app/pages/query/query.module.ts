import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { QueryRoutingModule } from './query-routing.module';
import { AddQueryComponent } from './add-query/add-query.component';
import { ManageQueriesComponent } from './manage-queries/manage-queries.component';
import { QueryComponent } from './query.component';
import {
  NbAccordionModule,
  NbButtonModule,
  NbCardModule,
  NbListModule,
  NbRouteTabsetModule,
  NbStepperModule,
  NbRadioModule,
  NbSelectModule,
  NbUserModule,
} from '@nebular/theme';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { NbIconModule, NbInputModule, NbTreeGridModule } from '@nebular/theme';

@NgModule({
  declarations: [
    QueryComponent,
    AddQueryComponent,
    ManageQueriesComponent,
  ],
  imports: [
    CommonModule,
    QueryRoutingModule,
    NbAccordionModule,
    NbButtonModule,
    NbCardModule,
    NbListModule,
    NbRouteTabsetModule,
    NbStepperModule,
    FormsModule, ReactiveFormsModule,
    NbRadioModule,
    NbSelectModule,
    NbUserModule,
    Ng2SmartTableModule,
    NbIconModule,
    NbInputModule,
    NbTreeGridModule
  ],
})
export class QueryModule { }
