import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Profil } from '../profil/profil.module';

@Injectable({
  providedIn: 'root'
})
export class ProfilService {

  private apiUrl = 'http://127.0.0.1:5000/api/profil/all'; 

  constructor(private http: HttpClient) { }

  getProfiles(): Observable<Profil[]> {
    return this.http.get<Profil[]>(this.apiUrl);
  }
}
