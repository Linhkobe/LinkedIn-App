import { Component, OnInit } from '@angular/core';
import { SharedService } from '../shared.service';

@Component({
  selector: 'app-donnees',
  templateUrl: './donnees.component.html'
})
export class DonneesComponent implements OnInit {
  constructor(public sharedService: SharedService) {}

  ngOnInit() {}
}
