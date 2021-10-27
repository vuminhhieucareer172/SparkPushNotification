import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddStreamComponent } from './add-stream/add-stream.component';
import { StreamingComponent } from './streaming.component';
import { ManageStreamsComponent } from "./manage-streams/manage-streams.component";

const routes: Routes = [
  { path: '', component: StreamingComponent },
  { path: 'add-stream', component: AddStreamComponent },
  { path: 'manage-streams', component: ManageStreamsComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StreamingRoutingModule { }
