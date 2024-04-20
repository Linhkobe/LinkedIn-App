import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-import-file',
  templateUrl: './import-file.component.html',
  styleUrl: './import-file.component.scss'
})
export class ImportFileComponent {
  isLoading = false;
  private checkDatabaseStatusSubscription: Subscription | undefined;

  file = {
    name: '', 
    progress: 0,
    size: 0,
  };

  constructor(private http: HttpClient, private router:Router) { }


  @ViewChild('fileDropRef', { static: false }) fileDropEl!: ElementRef<HTMLInputElement>;

  checkDatabaseStatus() {
    this.checkDatabaseStatusSubscription = interval(5000).subscribe({
      next: () => {
        this.http.get<any>('http://localhost:5000/check-database-status')
          .subscribe({
            next: (response) => {
              if (response && response.status === 'done') {
                // If the database is ready, stop checking and display the content
                this.isLoading = false;
                this.checkDatabaseStatusSubscription?.unsubscribe();
              }
            },
            error: (error) => {
              console.error('Error checking database status', error);
            }
          });
      }
    });
  }
  

  onDragOver(evt: DragEvent) {
    evt.preventDefault();
    evt.stopPropagation();
  }

  onDragLeave(evt: DragEvent) {
    evt.preventDefault();
    evt.stopPropagation();

  }

  onDrop(evt: DragEvent) {
    evt.preventDefault();
    evt.stopPropagation();
    const files = evt.dataTransfer?.files;
    if (files && files.length === 1 && files[0].type === 'application/json') {
      this.fileDropEl.nativeElement.files = files;
      this.file.name = files[0].name; 
      this.file.size = files[0].size;
      this.uploadFileSimulator(); 
    } else {
      alert('Please drop only one JSON file.');
    }
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length === 1 && input.files[0].type === 'application/json') {
      this.file.name = input.files[0].name; 
      this.file.size = input.files[0].size; 
    } else {
      alert('Please select only one JSON file.');
    }
    this.uploadFileSimulator();
  }

  uploadFileSimulator() {
    if (this.file.progress === 100) {
      return;
    } else {
      const progressInterval = setInterval(() => {
        if (this.file.progress === 100) {
          clearInterval(progressInterval);
        } else {
          this.file.progress += 5;
        }
      }, 200);
    }
  }


  formatBytes(bytes: number, decimals: number): string {
    if (bytes === 0) {
      return '0 Bytes';
    }
    const k = 1024;
    const dm = decimals <= 0 ? 0 : decimals || 2;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  deleteFile(){
    this.file.name = '';
    this.file.size = 0;
    this.file.progress = 0;

    if (this.fileDropEl && this.fileDropEl.nativeElement) {
      this.fileDropEl.nativeElement.value = '';
    }

  }

  onInsertClick() {
    this.isLoading = true;
    const formData = new FormData();
    if (this.fileDropEl && this.fileDropEl.nativeElement && this.fileDropEl.nativeElement.files && this.fileDropEl.nativeElement.files[0]) {
      formData.append('file', this.fileDropEl.nativeElement.files[0]);
    }
  
    this.http.post('http://localhost:5000/execute-script', formData)
    .subscribe({
      next: (response) => {
        console.log('Python script executed successfully', response);
        this.checkDatabaseStatus();
        alert("Database filled successfully");
      },
      error: (error) => {
        console.error('Error executing Python script', error);
      }
    });
  }
  ngOnDestroy() {
    this.checkDatabaseStatusSubscription?.unsubscribe();
  }
}
