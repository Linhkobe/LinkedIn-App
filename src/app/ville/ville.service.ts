import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ville } from './ville.module';

@Injectable({
  providedIn: 'root'
})
export class VilleService {

  private apiUrl = 'http://127.0.0.1:5000/api/ville/all'; 

  constructor(private http: HttpClient) { }

  getVilles(): Observable<ville[]> {
    return this.http.get<ville[]>(this.apiUrl);
  }
}
