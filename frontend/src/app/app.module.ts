import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from "@angular/common/http";
import { FormsModule } from "@angular/forms";
import { SidebarComponent } from './sidebar/sidebar.component';
import { TopbarComponent } from './topbar/topbar.component';
import { StreamingComponent } from './streaming/streaming.component';
import { QueryComponent } from './query/query.component';
import { ConfigurationsComponent } from './configurations/configurations.component';
import { JobStreamComponent } from './job-stream/job-stream.component';
import { DatabaseConnectionComponent } from './database-connection/database-connection.component';
import { FooterComponent } from './footer/footer.component';

@NgModule({
  declarations: [
    AppComponent,
    SidebarComponent,
    TopbarComponent,
    StreamingComponent,
    QueryComponent,
    ConfigurationsComponent,
    JobStreamComponent,
    DatabaseConnectionComponent,
    FooterComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
