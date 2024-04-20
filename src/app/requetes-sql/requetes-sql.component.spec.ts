import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RequetesSqlComponent } from './requetes-sql.component';

describe('RequetesSqlComponent', () => {
  let component: RequetesSqlComponent;
  let fixture: ComponentFixture<RequetesSqlComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RequetesSqlComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RequetesSqlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
