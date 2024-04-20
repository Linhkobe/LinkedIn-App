import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExpeentreComponent } from './expeentre.component';

describe('ExpeentreComponent', () => {
  let component: ExpeentreComponent;
  let fixture: ComponentFixture<ExpeentreComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExpeentreComponent]
    });
    fixture = TestBed.createComponent(ExpeentreComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
