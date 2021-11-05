import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddQueryComponent } from './add-query/add-query.component';
import { ManageQueriesComponent } from './manage-queries/manage-queries.component';
import { QueryComponent } from './query.component';

const routes: Routes = [{
  path: '',
  component: QueryComponent,
  children: [
    {
      path: 'add-query',
      component: AddQueryComponent,
    },
    {
      path: 'manage-queries',
      component: ManageQueriesComponent,
    },
  ],

}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class QueryRoutingModule { }
