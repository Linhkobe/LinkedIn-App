import { Router } from '@angular/router';
import { Component, OnInit, ElementRef, ViewChild, TemplateRef } from '@angular/core';
import { DataService } from '../data.service';
import { DashboardInfo, Domain, DureeJob, Expcom, Expentre, Job } from './db.module';
import { Chart, registerables } from 'chart.js';
import { LinearScale, CategoryScale } from 'chart.js';
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot';
import { MatDialog, MatDialogConfig, MatDialogRef } from '@angular/material/dialog';
import { AfterViewInit } from '@angular/core';
enum ChartType {
  Bar = 'bar',
  Pie = 'pie',
  Line = 'line',
  Boxplot = 'boxplot'
}
Chart.register(...registerables);
Chart.register(BoxPlotController, BoxAndWiskers, LinearScale, CategoryScale);

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit, AfterViewInit {
  dashboardInfo: { label: string; value: string | number }[] = [];
  @ViewChild('wordcloud') private wordcloudContainer!: ElementRef;
  @ViewChild('dialogTemplate') dialogTemplate: TemplateRef<any>;
  competenceChart: any;
  entrepriseChart: any;
  domainChart: any;
  yeardiplomeChart: any;
  dureejobChart:any;
  jobChart: any;
  topentreprise: Expentre[] = [];
  topcompetence: Expcom[] = [];
  topdomaine : Domain[] = [];
  topjob: Job[] = [];
  dureejob: DureeJob[] = [];
  numStudents: number; 
  numExperiences: number;
  numEntreprises: number;
  numCompetences: number;
  dialogRef: MatDialogRef<any>;
  selectedCharts: ChartType[] = [];

// Update these variables when checkboxes are selected

  charts = [
    { name: 'Top Competences', type: ChartType.Bar, limit: 10, enabled: false },
    { name: 'Top Entreprises', type: ChartType.Pie, limit: 5, enabled:false },
    { name: 'Top Domain', type: ChartType.Bar, enabled: false },
    { name: 'Année d\'obtention du diplôme', type: ChartType.Line, enabled: false},
    { name: 'Durée d\'expérience', type: ChartType.Boxplot, enabled: false}
  ];
  


  constructor(private router: Router,
    private dataService:DataService, public dialog: MatDialog) {}

    resetChart() {
      // Reset all the charts
      if (this.competenceChart) {
        this.competenceChart.data.labels = [];
        this.competenceChart.data.datasets = [];
        this.competenceChart.update();
      }
    
      if (this.entrepriseChart) {
        this.entrepriseChart.data.labels = [];
        this.entrepriseChart.data.datasets = [];
        this.entrepriseChart.update();
      }
    
      if (this.domainChart) {
        this.domainChart.data.labels = [];
        this.domainChart.data.datasets = [];
        this.domainChart.update();
      }
    
      if (this.yeardiplomeChart) {
        this.yeardiplomeChart.data.labels = [];
        this.yeardiplomeChart.data.datasets = [];
        this.yeardiplomeChart.update();
      }
    
      if (this.dureejobChart) {
        this.dureejobChart.data.labels = [];
        this.dureejobChart.data.datasets = [];
        this.dureejobChart.update();
      }
    }

    ngAfterViewInit() {
      // After the view has been initialized, set the flags to true
      this.competenceChart = true;
      this.entrepriseChart = true;
      this.domainChart = true;
      this.yeardiplomeChart = true;
      this.dureejobChart = true;
    }

    loadDashboardInfo() {
      // Assuming you have API endpoints like these, adjust accordingly
      this.dataService.getStudentCount().subscribe(data => {
        this.dashboardInfo.push({ label: 'Nombre d\'étudiants', value: data });
      });
  
      this.dataService.getExperienceCount().subscribe(data => {
        this.dashboardInfo.push({ label: 'Nombre d\'expériences', value: data });
      });
  
      this.dataService.getCompanyCount().subscribe(data => {
        this.dashboardInfo.push({ label: 'Nombre d\'entreprises', value: data });
      });
  
      this.dataService.getCompetenceCount().subscribe(data => {
        this.dashboardInfo.push({ label: 'Nombre de compétences', value: data });
      });
    }
    

  ngOnInit() {
    // this.loadCompetenceData();
    // this.loadEntrepriseData();
    // this.loadExeperienceData();
    this.loadDashboardInfo();
  }

  toggleChartSelection(chartType: ChartType) {
    const index = this.selectedCharts.indexOf(chartType);
    if (index === -1) {
      this.selectedCharts.push(chartType);
    } else {
      this.selectedCharts.splice(index, 1);
    }
  }
  showSelectedCharts() {
    this.charts.forEach(chart => {
      if (chart.enabled) {
        switch (chart.name) {
          case 'Top Competences':
            this.loadCompetenceData(chart);
            break;
          case 'Top Entreprises':
            this.loadEntrepriseData(chart);
            break;
          case 'Top Domain':
            this.loadDomainData(chart);
            break;
          case 'Année d\'obtention du diplôme':
            this.loadYearDiplomeData(chart);
            break;
          case 'Durée d\'expérience':
            this.loadDureeJobData(chart);
            break;
        }
      }
    });
    this.resetCharts();
    
  }
  resetCharts() {
    // Clear the data from all the charts
    this.destroyChart(this.competenceChart);
    this.destroyChart(this.entrepriseChart);
    this.destroyChart(this.domainChart);
    this.destroyChart(this.yeardiplomeChart);
    this.destroyChart(this.dureejobChart);

    // Close the dialog
    if (this.dialogRef) {
      this.dialogRef.close();
    }
  }

  destroyChart(chart: any) {
    if (chart instanceof Chart) {
      chart.destroy();
    }
  }
  loadCompetenceData(chartConfig) {
    this.dataService.getTopCompetences(chartConfig.limit).subscribe(data => {
      this.drawChart('competenceChart', chartConfig.type, 'competence', data.slice(0, chartConfig.limit));
    });
  }
  
  loadEntrepriseData(chartConfig) {
    this.dataService.getTopEntreprises(chartConfig.limit).subscribe(data => {
      this.drawChart('entrepriseChart', chartConfig.type, 'entreprise', data.slice(0, chartConfig.limit));
    });
  }

  loadDomainData(chartConfig) {
    this.dataService.getDomain().subscribe(data => {
      this.drawChart('domainChart', chartConfig.type, 'experience_pro', data.slice(0, chartConfig.limit));
    });
  }

  loadYearDiplomeData(chartConfig) {
    this.dataService.getYearDiplome().subscribe(data => {
      this.drawChart('yeardiplomeChart', chartConfig.type, 'education', data.slice(0, chartConfig.limit));
    });
  }

  loadDureeJobData(chartConfig) {
    this.dataService.getDurationExperience().subscribe(data => {
      this.drawChart('dureejobChart', chartConfig.type, 'experience_pro', data);
    });
  }
  

  openDialog(): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.autoFocus = true;
    dialogConfig.width = '250px';
    this.dialog.open(this.dialogTemplate, dialogConfig);
  }

  drawChart(canvasId: string, chartType: ChartType, dataType: string, data: any) {
    let labels, chartLabel;
  
    // Check if the data is for a boxplot
    const isBoxplot = chartType === ChartType.Boxplot;
    const selectedChartsContainer = document.getElementById('selectedChartsContainer');
    const isSelected = this.selectedCharts.includes(chartType);

    if (isSelected) {
      const selectedChartDiv = document.createElement('div');
      selectedChartDiv.classList.add('chart');
      selectedChartDiv.innerHTML = `<canvas id="${canvasId}"></canvas>`;
      selectedChartsContainer.appendChild(selectedChartDiv);
    }

    if (canvasId === 'dureejobChart') {
      chartType = ChartType.Boxplot;
    }
  
    if (isBoxplot) {
      // For boxplot, data should include min, q1, median, q3, and max
      labels = ['Boxplot'];
      chartLabel = 'Durée d\'expérience';
    } else {
      // For other chart types (bar, pie, etc.)
      if (dataType === 'competence') {
        labels = data.map(item => item.nom_competence);
        chartLabel = 'Top Competences';
      } else if (dataType === 'entreprise') {
        labels = data.map(item => item.nom);
        chartLabel = 'Top Entreprises';
      } else if (dataType === 'experience_pro') {
        labels = data.map(item => item.domaine);
        chartLabel = 'Top Domain';
      } else if (dataType === 'education') {
        labels = data.map(item => item.annee_diplome);
        chartLabel = 'Année d\'obtention du diplôme';
      } else if (dataType === 'experience_pro') {
        labels = data.map(item => item.duration_num);
        chartLabel = 'Durée d\'expérience';
      }
    }
  
    // Get the canvas element
    const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
  
    // If a chart already exists on the canvas, destroy it
    if (canvas && canvas['chart']) {
      canvas['chart'].destroy();
    }
  
    // Configure chart options based on chart type
    const chartOptions = isBoxplot
      ? {
          scales: {
            x: {
              beginAtZero: true,
            },
          },
        }
      : {
          plugins: {
            title: {
              display: true,
              text: chartLabel,
              font: {
                size: 18,
              },
            },
          },
        };
  
    const chart = new Chart(canvasId, {
      type: isBoxplot ? 'boxplot' : chartType,
      data: {
        labels: labels,
        datasets: isBoxplot
          ? [
              {
                label: chartLabel,
                data: [data], // Boxplot data should be an array of arrays
                borderColor: 'rgb(72, 175, 193)',
                borderWidth: 2,
                outlierRadius: 5,
              },
            ]
          : [
              {
                label: chartLabel,
                data: data.map(item => item.count || item.proportion),
                backgroundColor: chartType === 'bar' ? 'rgb(72, 175, 193)' : undefined,
              },
            ],
      },
      // options: { ...chartOptions, indexAxis: 'y' },
      options: chartOptions,
    });
  
    if (canvas) {
      canvas['chart'] = chart;
    }
  
    // Store the chart instance in the corresponding variable
    switch (canvasId) {
      case 'competenceChart':
        this.competenceChart = chart;
        break;
      case 'entrepriseChart':
        this.entrepriseChart = chart;
        break;
      case 'domainChart':
        this.domainChart = chart;
        break;
      case 'yeardiplomeChart':
        this.yeardiplomeChart = chart;
        break;
      case 'dureejobChart':
        this.dureejobChart = chart;
        break;
    }
  }
  

  onClick() {
    // Navigate to the new route
    this.router.navigate(['/dashboard']);
  }

}