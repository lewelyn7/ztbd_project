import { Component, Injectable } from '@angular/core';
import { TestCaseComponent } from './components/test-case/test-case.component';
import { HttpClient, HttpParams } from '@angular/common/http';
import { HtmlParser } from '@angular/compiler';
import { environment } from 'src/environments/environment';
import { ChartResult, StaticSettings, TestCase } from './models';
import { BoxChartComponent } from '@swimlane/ngx-charts';
import { max } from 'rxjs';
@Injectable()
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'db-perf-tester';
  chartSize: [number, number] = [700, 600]
  iterations: number = 10
  displayedColumns: string[] = ['database', 'max', 'min', 'mean', 'std_dev'];
  tableData = [
    {database: "mongodb", "max": -1, "min": -1, "mean": -1, "std_dev": -1}
  ]
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
        description: "Indexed search",
        staticSettings:{
          url: environment.backendUrl + 'tests/0'
        }
      },
      {
        name: "Case1",
        description: "unindexed search",
        staticSettings:{
          url: environment.backendUrl + 'tests/1'
        }
      },
      {
        name: "Case2",
        description: "Not exist element",
        staticSettings:{
          url: environment.backendUrl + 'tests/2'
        }
      },
      {
        name: "Case3",
        description: "Find review by part of opinion",
        staticSettings:{
          url: environment.backendUrl + 'tests/3'
        }
      }
    ]
  
  onTestResult(result: ChartResult){
    console.log("app", result)
    this.testResults = result
    this.tableData = this.chartResultToTableData(result)
    // let r = result as ChartResult
    // console.log(r)
  }

  chartResultToTableData(result: ChartResult){
    let data = []
    for(let series of result.data){
      let helper = [...series.series.map(v => v.value)]
      const max = Math.max(...series.series.map(v => v.value))
      const min = Math.min(...series.series.map(v => v.value))
      const mean = helper.reduce((a,b) => a+b, 0) / helper.length
      const std_dev = Math.sqrt(helper.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / helper.length)
      data.push({
        database: series.name,
        max: max,
        min: min,
        mean: mean,
        std_dev: std_dev
      })
    }
    return data
  }
}
