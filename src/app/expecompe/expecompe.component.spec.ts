import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExpecompeComponent } from './expecompe.component';

describe('ExpecompeComponent', () => {
  let component: ExpecompeComponent;
  let fixture: ComponentFixture<ExpecompeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExpecompeComponent]
    });
    fixture = TestBed.createComponent(ExpecompeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
