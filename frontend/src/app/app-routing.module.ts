import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'stream', loadChildren: () => import('./streaming/streaming.module').then(m => m.StreamingModule ) },
  { path: 'query', loadChildren: () => import('./query/query.module').then(m => m.QueryModule ) },
  { path: 'configurations', loadChildren: () => import('./configurations/configurations.module').then(m => m.ConfigurationsModule ) },
  { path: 'job-stream', loadChildren: () => import('./job-stream/job-stream.module').then(m => m.JobStreamModule ) },
  { path: 'database-connection', loadChildren: () => import('./database-connection/database-connection.module').then(m => m.DatabaseConnectionModule ) },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
