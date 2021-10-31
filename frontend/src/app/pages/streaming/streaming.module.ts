import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { StreamingRoutingModule } from './streaming-routing.module';
import { AddStreamComponent } from './add-stream/add-stream.component';
import { ManageStreamsComponent } from './manage-streams/manage-streams.component';
import { NbButtonModule, NbCardModule, NbCheckboxModule, NbInputModule, NbIconModule, NbSelectModule } from '@nebular/theme';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { ReactiveFormsModule } from "@angular/forms";


@NgModule({
  declarations: [
    AddStreamComponent,
    ManageStreamsComponent,
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
        NbSelectModule
    ],
})
export class StreamingModule { }
