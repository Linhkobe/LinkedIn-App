import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { Experiences } from './experience.module';

@Component({
  selector: 'app-experience',
  templateUrl: './experience.component.html',
  styleUrls: ['./experience.component.scss']
})
export class ExperienceComponent {
  experiences: Experiences[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getExperiences().subscribe((data: any[]) => {
      console.log('Received data:', data);
      this.experiences = data;
    });
  }
}

