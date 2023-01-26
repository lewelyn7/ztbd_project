import { Component, Injectable } from '@angular/core';
import { TestCaseComponent } from './components/test-case/test-case.component';
import { HttpClient, HttpParams } from '@angular/common/http';
import { HtmlParser } from '@angular/compiler';
import { environment } from 'src/environments/environment';
import { ChartResult, StaticSettings, TestCase } from './models';
import { BoxChartComponent } from '@swimlane/ngx-charts';
@Injectable()
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'db-perf-tester';
  iterations: number = 10
  testResults: ChartResult = {data:[
    {
      "name": "mongo",
      "series": [
          {name: "0", value: 0},
          {name: "1", value: 100},
          {name: "2", value: 250},
      ]
    },
    {
      "name": "postgresql",
      "series": [
          {name: "0", value: 0},
          {name: "1", value: 100},
          {name: "2", value: 250},
      ]
    }
  ]
}
  testCases: TestCase[] = [
      {
        name: "Case0",
        staticSettings:{
          url: environment.backendUrl + 'tests/0'
        }
      }
    ]
  
  onTestResult(result: ChartResult){
    console.log("app", result)
    this.testResults = result
    // let r = result as ChartResult
    // console.log(r)
  }
}
