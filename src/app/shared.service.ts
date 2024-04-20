import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  private showTabsSubject = new BehaviorSubject<boolean>(false);
  
  showTabs$ = this.showTabsSubject.asObservable();

  setShowTabs(value: boolean) {
    this.showTabsSubject.next(value);
  }
  constructor() { }
}
