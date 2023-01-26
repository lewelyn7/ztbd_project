import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatToolbarModule} from '@angular/material/toolbar'; 
import {MatCardModule} from '@angular/material/card'; 
import {MatButtonModule} from '@angular/material/button'; 
import {MatDividerModule} from '@angular/material/divider';
import { TestCaseComponent } from './components/test-case/test-case.component'
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner'; 
import { HttpClientModule } from '@angular/common/http';
import {MatInputModule} from '@angular/material/input'; 
import { BoxChartModule } from '@swimlane/ngx-charts';
@NgModule({
  declarations: [
    AppComponent,
    TestCaseComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatCardModule,
    MatButtonModule,
    MatDividerModule,
    MatProgressSpinnerModule,
    HttpClientModule,
    FormsModule,
    MatInputModule,
    BoxChartModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
