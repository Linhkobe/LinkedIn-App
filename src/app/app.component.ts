import { Component, ViewChild, TemplateRef } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { SharedService } from './shared.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'linkedinApp';
  opened = false;

  @ViewChild('dialogTemplate') dialogTemplate: TemplateRef<any>;

  constructor(public dialog: MatDialog, private sharedService: SharedService) {}

  openDialog(): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;
    dialogConfig.width = '250px';
    this.dialog.open(this.dialogTemplate, dialogConfig);
  }

  setShowTabs(value: boolean) {
    this.sharedService.setShowTabs(value);
  }
}
