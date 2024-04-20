import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { Competences } from './competence.module';

@Component({
  selector: 'app-competence',
  templateUrl: './competence.component.html',
  styleUrls: ['./competence.component.scss']
})
export class CompetenceComponent {
  competences: Competences[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getCompetences().subscribe(data => {
      this.competences = data;
    });
  }
}

