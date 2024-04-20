import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Educations } from '../education/education.module';

@Injectable({
  providedIn: 'root'
})
export class EducationListService {

  private apiUrl = 'http://127.0.0.1:5000/api/education/all'; 

  constructor(private http: HttpClient) { }

  getEducations(): Observable<Educations[]> {
    return this.http.get<Educations[]>(this.apiUrl);
  }
}
