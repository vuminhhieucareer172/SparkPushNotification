import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { StreamingRoutingModule } from './streaming-routing.module';
import { AddStreamComponent } from './add-stream/add-stream.component';
import { ManageStreamsComponent } from './manage-streams/manage-streams.component';
import { NbButtonModule, NbCardModule, NbCheckboxModule, NbInputModule, NbIconModule, NbSelectModule } from '@nebular/theme';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { ReactiveFormsModule } from '@angular/forms';
import { StreamingComponent } from './streaming.component';
import { DetailStreamComponent } from './detail-stream/detail-stream.component';
import { RecordComponent } from './detail-stream/record/record.component';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    StreamingComponent,
    AddStreamComponent,
    ManageStreamsComponent,
    DetailStreamComponent,
    RecordComponent,
  ],
  imports: [
    CommonModule,
    StreamingRoutingModule,
    NbCardModule,
    NbCheckboxModule,
    NbInputModule,
    NbButtonModule,
    Ng2SmartTableModule,
    ReactiveFormsModule,
    NbIconModule,
    NbSelectModule,
    FormsModule,
  ],
})
export class StreamingModule { }
