import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { QueryRoutingModule } from './query-routing.module';
import { AddQueryComponent } from './add-query/add-query.component';
import { ManageQueriesComponent } from './manage-queries/manage-queries.component';
import { QueryComponent } from './query.component';


@NgModule({
  declarations: [
    QueryComponent,
    AddQueryComponent,
    ManageQueriesComponent,
  ],
  imports: [
    CommonModule,
    QueryRoutingModule,
  ],
})
export class QueryModule { }
