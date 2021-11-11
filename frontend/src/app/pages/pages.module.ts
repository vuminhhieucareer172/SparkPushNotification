import { NgModule } from '@angular/core';
import { NbMenuModule } from '@nebular/theme';

import { ThemeModule } from '../@theme/theme.module';
import { PagesComponent } from './pages.component';
import { DashboardModule } from './dashboard/dashboard.module';
import { ECommerceModule } from './e-commerce/e-commerce.module';
import { DatabaseConnectionModule } from './database-connection/database-connection.module';
import { ConfigurationsModule } from './configurations/configurations.module';

import { PagesRoutingModule } from './pages-routing.module';
import { MiscellaneousModule } from './miscellaneous/miscellaneous.module';
import { ConfigurationsComponent } from './configurations/configurations.component';
import { DatabaseConnectionComponent } from './database-connection/database-connection.component';

@NgModule({
  imports: [
    PagesRoutingModule,
    ThemeModule,
    NbMenuModule,
    DashboardModule,
    ECommerceModule,
    MiscellaneousModule,
    DatabaseConnectionModule,
    // ConfigurationsModule,
  ],
  declarations: [
    PagesComponent,
    // ConfigurationsComponent,
  ],
})
export class PagesModule {
}
