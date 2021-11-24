import { NgModule } from '@angular/core';
import { NbMenuModule } from '@nebular/theme';

import { ThemeModule } from '../@theme/theme.module';
import { PagesComponent } from './pages.component';
import { DashboardModule } from './dashboard/dashboard.module';
import { ECommerceModule } from './e-commerce/e-commerce.module';
import { DatabaseConnectionModule } from './database-connection/database-connection.module';

import { PagesRoutingModule } from './pages-routing.module';
import { MiscellaneousModule } from './miscellaneous/miscellaneous.module';
import { DatabaseConnectionComponent } from './database-connection/database-connection.component';
import { ConfigurationsComponent } from './configurations/configurations.component';
import { ConfigurationsModule } from './configurations/configurations.module';
import { Query1Component } from './query1/query1.component';
import { AddQueryComponent } from './query1/add-query/add-query.component';

@NgModule({
  imports: [
    PagesRoutingModule,
    ThemeModule,
    NbMenuModule,
    DashboardModule,
    ECommerceModule,
    MiscellaneousModule,
    DatabaseConnectionModule,
    ConfigurationsModule,
  ],
  declarations: [
    PagesComponent,
    // Query1Component,
    // AddQueryComponent,
    // Configurations1Component,
    // ConfigurationsComponent,
  ],
})
export class PagesModule {
}
