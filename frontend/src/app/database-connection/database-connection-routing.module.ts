import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DatabaseConnectionComponent } from "./database-connection.component";

const routes: Routes = [
  { path: '', component: DatabaseConnectionComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DatabaseConnectionRoutingModule { }
