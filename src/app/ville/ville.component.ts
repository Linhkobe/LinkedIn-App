import { Component } from '@angular/core';
import { DataService } from '../data.service';
import { ville } from './ville.module';
import { VilleService } from './ville.service';

@Component({
  selector: 'app-ville',
  templateUrl: './ville.component.html',
  styleUrl: './ville.component.scss'
})
export class VilleComponent {
  villes: ville[] = [];
  constructor(private dataService: DataService, private villeService: VilleService) {}

  ngOnInit(): void {
    this.dataService.getVilles().subscribe((data: any[]) => {
      console.log('Received data:', data);
      this.villes = data;
    });
  }
}
