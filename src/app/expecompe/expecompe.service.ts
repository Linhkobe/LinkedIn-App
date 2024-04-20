import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Expecompe } from '../expecompe/expecompe.module';

@Injectable({
  providedIn: 'root'
})
export class ExpecompeService {

  private apiUrl = 'http://127.0.0.1:5000/api/expcom/all'; 

  constructor(private http: HttpClient) { }

  getExperienceCompetence(): Observable<Expecompe[]> {
    return this.http.get<Expecompe[]>(this.apiUrl);
  }
}
