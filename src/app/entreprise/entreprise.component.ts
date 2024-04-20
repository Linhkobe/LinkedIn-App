import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { Entreprise } from './entreprise.module';

@Component({
  selector: 'app-entreprise',
  templateUrl: './entreprise.component.html',
  styleUrls: ['./entreprise.component.scss']
})
export class EntrepriseComponent {
  entreprises: Entreprise[] = [];

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getEntreprises().subscribe((data: any[]) => {
      console.log('Received data:', data);
      this.entreprises = data;
    });
  }
}

