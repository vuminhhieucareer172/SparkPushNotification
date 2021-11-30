import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddQueryComponent } from './add-query/add-query.component';
import { ManageQueriesComponent } from './manage-queries/manage-queries.component';
import { Query1Component } from './query1.component';
import { DetailQueryComponent } from './detail-query/detail-query.component';

const routes: Routes = [{
  path: '',
  component: Query1Component,
  children: [
    {
      path: 'add-query',
      component: AddQueryComponent,
    },
    {
      path: 'manage-queries',
      component: ManageQueriesComponent,
    },
    {
      path: 'detail/:queryId',
      component: DetailQueryComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class QueryRoutingModule { }
