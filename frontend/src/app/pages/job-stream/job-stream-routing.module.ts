import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { JobStreamComponent } from './job-stream.component';
import { ManageComponent } from './manage/manage.component';

const routes: Routes = [{
  path: '',
  component: JobStreamComponent,
  children: [
    {
      path: 'manage',
      component: ManageComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class JobStreamRoutingModule { }
