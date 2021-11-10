import { NgModule } from '@angular/core';
import {
  NbActionsModule,
  NbButtonModule,
  NbCardModule,
  NbTabsetModule,
  NbUserModule,
  NbRadioModule,
  NbSelectModule,
  NbListModule,
  NbIconModule,
  NbInputModule,
} from '@nebular/theme';
import { NgxEchartsModule } from 'ngx-echarts';
import { Ng2SmartTableModule } from 'ng2-smart-table';

import { ThemeModule } from '../../@theme/theme.module';
import { ConfigurationsComponent } from './configurations.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AddConfigurationsComponent } from './add-configurations/add-configurations.component';
import { ConfigurationsRoutingModule } from './configurations-routing.module';
import { ManageConfigurationsComponent } from './manage-configurations/manage-configurations.component';

@NgModule({
  imports: [
    FormsModule,
    ThemeModule,
    NbCardModule,
    NbUserModule,
    NbButtonModule,
    NbTabsetModule,
    NbActionsModule,
    NbRadioModule,
    NbSelectModule,
    NbListModule,
    NbIconModule,
    NbButtonModule,
    NgxEchartsModule,
    NbInputModule,
    ReactiveFormsModule,
    Ng2SmartTableModule,
    ConfigurationsRoutingModule,
  ],
  declarations: [
    ConfigurationsComponent,
    AddConfigurationsComponent,
    ManageConfigurationsComponent,
  ],
})
export class ConfigurationsModule { }
