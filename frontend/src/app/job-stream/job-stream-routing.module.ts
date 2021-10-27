import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { JobStreamComponent } from "./job-stream.component";

const routes: Routes = [
  { path: '', component: JobStreamComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobStreamRoutingModule { }
