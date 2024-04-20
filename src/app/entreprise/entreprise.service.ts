import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Entreprise } from '../entreprise/entreprise.module';

@Injectable({
  providedIn: 'root'
})
export class EntrepriseService {

  private apiUrl = 'http://127.0.0.1:5000/api/entreprise/all'; 

  constructor(private http: HttpClient) { }

  getEntreprises(): Observable<Entreprise[]> {
    return this.http.get<Entreprise[]>(this.apiUrl);
  }
}

