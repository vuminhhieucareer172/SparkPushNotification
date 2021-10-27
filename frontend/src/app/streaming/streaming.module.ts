import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { StreamingRoutingModule } from './streaming-routing.module';
import { AddStreamComponent } from './add-stream/add-stream.component';
import { ManageStreamsComponent } from './manage-streams/manage-streams.component';


@NgModule({
  declarations: [
    AddStreamComponent,
    ManageStreamsComponent
  ],
  imports: [
    CommonModule,
    StreamingRoutingModule
  ]
})
export class StreamingModule { }
