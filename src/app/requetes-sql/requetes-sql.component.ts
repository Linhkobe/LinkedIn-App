import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-requetes-sql',
  templateUrl: './requetes-sql.component.html'
})
export class RequetesSqlComponent {
  constructor(private router: Router) {}

  // Method to handle the click event
  onClick() {
    // Navigate to the new route
    this.router.navigate(['/requeteSQL']);
  }
}
