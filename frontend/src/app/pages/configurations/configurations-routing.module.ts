import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ConfigurationsComponent } from './configurations.component';
import { AddConfigurationsComponent } from './add-configurations/add-configurations.component';
import { ManageConfigurationsComponent } from './manage-configurations/manage-configurations.component';

const routes: Routes = [{
  path: '',
  component: ConfigurationsComponent,
  children: [
    {
      path: 'add-config',
      component: AddConfigurationsComponent,
    },
    {
      path: 'manage-config',
      component: ManageConfigurationsComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class ConfigurationsRoutingModule { }
