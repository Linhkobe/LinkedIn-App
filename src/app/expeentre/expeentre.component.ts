import { Component } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-expeentre',
  templateUrl: './expeentre.component.html',
  styleUrls: ['./expeentre.component.scss']
})
export class ExpeentreComponent {
  expeentres: any[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getExperienceEntreprise().subscribe((data: any[]) => {
      console.log('Received data:', data);
      this.expeentres = data;
    });
  }
}

