import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dataviz',
  standalone: true,
  imports: [],
  templateUrl: './dataviz.component.html',
  styleUrl: './dataviz.component.scss'
})
export class DatavizComponent {
  constructor(private router: Router) {}

  onClick() {
    // Navigate to the new route
    this.router.navigate(['/dataviz']);
  }
}
