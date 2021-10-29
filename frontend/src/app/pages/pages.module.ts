import { NgModule } from '@angular/core';
import { NbMenuModule } from '@nebular/theme';

import { ThemeModule } from '../@theme/theme.module';
import { PagesComponent } from './pages.component';
import { DashboardModule } from './dashboard/dashboard.module';
import { ECommerceModule } from './e-commerce/e-commerce.module';
import { PagesRoutingModule } from './pages-routing.module';
import { MiscellaneousModule } from './miscellaneous/miscellaneous.module';
import { StreamingComponent } from './streaming/streaming.component';
import { QueryComponent } from './query/query.component';
import { ConfigurationsComponent } from './configurations/configurations.component';
import { DatabaseConnectionComponent } from './database-connection/database-connection.component';
import { JobStreamComponent } from './job-stream/job-stream.component';

@NgModule({
  imports: [
    PagesRoutingModule,
    ThemeModule,
    NbMenuModule,
    DashboardModule,
    ECommerceModule,
    MiscellaneousModule,
  ],
  declarations: [
    PagesComponent,
    StreamingComponent,
    QueryComponent,
    ConfigurationsComponent,
    DatabaseConnectionComponent,
    JobStreamComponent,
  ],
})
export class PagesModule {
}
