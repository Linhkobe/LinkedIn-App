import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Experiences } from '../experience/experience.module';

@Injectable({
  providedIn: 'root'
})
export class ExperienceService {

  private apiUrl = 'http://127.0.0.1:5000/api/experience/all'; 

  constructor(private http: HttpClient) { }

  getExperiences(): Observable<Experiences[]> {
    return this.http.get<Experiences[]>(this.apiUrl);
  }
}
