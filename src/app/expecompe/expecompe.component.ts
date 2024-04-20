import { Component } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-expecompe',
  templateUrl: './expecompe.component.html',
  styleUrls: ['./expecompe.component.scss']
})
export class ExpecompeComponent {
  expecompes: any[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getExperienceCompetence().subscribe((data: any[]) => {
      console.log('Received data:', data);
      this.expecompes = data;
    });
  }
}

