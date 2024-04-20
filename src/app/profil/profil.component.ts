import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { Profil } from './profil.module';

@Component({
  selector: 'app-profil',
  templateUrl: './profil.component.html',
  styleUrls: ['./profil.component.scss'],
})
export class ProfilComponent implements OnInit {
  profiles: Profil[];
  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getProfiles()
    .subscribe(data => {
      this.profiles = data;
    });
  }
}
