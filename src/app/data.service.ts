import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { Profil } from './profil/profil.module';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  getProfiles(): Observable<Profil[]> {
    return this.http.get<Profil[]>(`${this.baseUrl}/profil/all`);
  }

  getCompetences(): Observable<any> {
    return this.http.get(`${this.baseUrl}/competence/all`);
  }

  getExperiences(): Observable<any> {
    return this.http.get(`${this.baseUrl}/experience/all`);
  }

  getEducations(): Observable<any> {
    return this.http.get(`${this.baseUrl}/education/all`);
  }

  getEntreprises(): Observable<any> {
    return this.http.get(`${this.baseUrl}/entreprise/all`);
  }

  getExperienceCompetence(): Observable<any> {
    return this.http.get(`${this.baseUrl}/expcom/all`);
  }

  getExperienceEntreprise(): Observable<any> {
    return this.http.get(`${this.baseUrl}/expentre/all`);
  }

  getTopCompetences(N:number): Observable<any> {
    return this.http.get(`${this.baseUrl}/top-competences/${N}/all`);
  }

  getTopEntreprises(N: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/top-entreprises/${N}/all`);
  }

  getVilles(): Observable<any> {
    return this.http.get(`${this.baseUrl}/ville/all`);
  }

  getTopJos(): Observable<any> {
    return this.http.get(`${this.baseUrl}/top-jobs/all`);
  }

  getDuration(): Observable<any> {
    return this.http.get(`${this.baseUrl}/duration/all`);
  }

  getNiveau(): Observable<any> {
    return this.http.get(`${this.baseUrl}/niveau_etude/all`);
  }

  getDashboardInfo(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/dashboard/info`);
  }

  getStudentCount(): Observable<number> {
    return this.http.get<number>(`${this.baseUrl}/dashboard/num_students`);
  }
  
  getExperienceCount(): Observable<number> {
    return this.http.get<number>(`${this.baseUrl}/dashboard/num_experiences`);
  }
  
  getCompanyCount(): Observable<number> {
    return this.http.get<number>(`${this.baseUrl}/dashboard/num_entreprises`);
  }
  
  getCompetenceCount(): Observable<number> {
    return this.http.get<number>(`${this.baseUrl}/dashboard/num_competences`);
  }

  getTopEducation(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/dashboard/top_education`);
  }

  getDomain(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/top-domaines/all`);
  }
  
  getYearDiplome(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/diplomes-par-annee/all`);
  }

  getDurationExperience(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/duree_job/all`);
  }
}


