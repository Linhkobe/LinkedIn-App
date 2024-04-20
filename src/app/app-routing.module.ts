import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DonneesComponent } from './donnees/donnees.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RequetesSqlComponent } from './requetes-sql/requetes-sql.component';
import { DatavizComponent } from './dataviz/dataviz.component';
import { ImportFileComponent } from './import-file/import-file.component';

const routes: Routes = [
  { path: '', redirectTo: 'import', pathMatch: 'full' },
  { path: 'home', component: DonneesComponent }, 
  { path: 'import', component: ImportFileComponent},
  { path: 'requeteSQL', component: RequetesSqlComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'donnees', component: DonneesComponent },
  { path: 'dataviz', component: DatavizComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
