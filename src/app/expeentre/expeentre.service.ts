import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Expeentre } from '../expeentre/expeentre.module';

@Injectable({
  providedIn: 'root'
})
export class ExpeentreService {

  private apiUrl = 'http://127.0.0.1:5000/api/expentre/all'; 

  constructor(private http: HttpClient) { }

  getExperienceEntreprise(): Observable<Expeentre[]> {
    return this.http.get<Expeentre[]>(this.apiUrl);
  }
}
