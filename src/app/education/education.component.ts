import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { Educations } from './education.module';

@Component({
  selector: 'app-education',
  templateUrl: './education.component.html',
  styleUrls: ['./education.component.scss']
})
export class EducationComponent implements OnInit {
  educations: Educations[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getEducations().subscribe((data: any[]) => {
      console.log('Received data:', data);
      this.educations = data;
    });
  }
}

