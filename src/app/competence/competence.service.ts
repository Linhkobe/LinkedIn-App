import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Competences } from '../competence/competence.module';

@Injectable({
  providedIn: 'root'
})
export class CompetenceService {

  private apiUrl = 'http://127.0.0.1:5000/api/competence/all'; 

  constructor(private http: HttpClient) { }

  getCompetences(): Observable<Competences[]> {
    return this.http.get<Competences[]>(this.apiUrl);
  }
}
