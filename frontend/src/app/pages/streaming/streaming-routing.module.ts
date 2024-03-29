import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StreamingComponent } from './streaming.component';
import { AddStreamComponent } from './add-stream/add-stream.component';
import { ManageStreamsComponent } from './manage-streams/manage-streams.component';
import { DetailStreamComponent } from './detail-stream/detail-stream.component';
import { RecordComponent } from './detail-stream/record/record.component';

const routes: Routes = [{
  path: '',
  component: StreamingComponent,
  children: [
    {
      path: 'add-stream',
      component: AddStreamComponent,
    },
    {
      path: 'manage-streams',
      component: ManageStreamsComponent,
    },
    {
      path: 'detail/:streamName',
      component: DetailStreamComponent,
    },
    {
      path: 'detail/:streamName/record',
      component: RecordComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class StreamingRoutingModule { }
