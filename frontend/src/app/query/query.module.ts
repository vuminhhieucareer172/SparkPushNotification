import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { QueryRoutingModule } from './query-routing.module';
import { AddQueryComponent } from './add-query/add-query.component';
import { ManageQueriesComponent } from './manage-queries/manage-queries.component';


@NgModule({
  declarations: [
    AddQueryComponent,
    ManageQueriesComponent
  ],
  imports: [
    CommonModule,
    QueryRoutingModule
  ]
})
export class QueryModule { }
