import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SidenavComponent } from './sidenav/sidenav.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { DonneesComponent } from './donnees/donnees.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatTabsModule } from '@angular/material/tabs';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {MatToolbarModule} from '@angular/material/toolbar';
import { HttpClientModule } from '@angular/common/http';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatListModule} from '@angular/material/list';
import { SharedService } from './shared.service';
import { ProfilComponent } from './profil/profil.component';
import { EducationComponent } from './education/education.component';
import { ExperienceComponent } from './experience/experience.component';
import { CompetenceComponent } from './competence/competence.component';
import { EntrepriseComponent } from './entreprise/entreprise.component';
import { ExpecompeComponent } from './expecompe/expecompe.component';
import { ExpeentreComponent } from './expeentre/expeentre.component';
import { VilleComponent } from './ville/ville.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { FormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';
import {ImportFileComponent} from './import-file/import-file.component';
import {ProgressComponent} from './progress/progress.component';

@NgModule({
  declarations: [
    AppComponent,
    SidenavComponent,
    ToolbarComponent,
    DonneesComponent,
    ProfilComponent,
    EducationComponent,
    ExperienceComponent,
    CompetenceComponent,
    EntrepriseComponent,
    ExpecompeComponent,
    ExpeentreComponent,
    VilleComponent,
    DashboardComponent,
    ImportFileComponent,
    ProgressComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatTabsModule,
    MatIconModule,
    MatButtonModule,
    MatToolbarModule, HttpClientModule, MatSidenavModule, MatListModule, FormsModule,
    MatDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
