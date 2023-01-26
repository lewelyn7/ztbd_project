import { HttpClient } from '@angular/common/http';
import { Component, Injectable, Input, Output, EventEmitter} from '@angular/core';
import { Observable } from 'rxjs';
import { ChartResult, ChartSeries, DataPoint, SingleDbResult, StaticSettings } from 'src/app/models';
import { forkJoin } from 'rxjs';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-test-case',
  templateUrl: './test-case.component.html',
  styleUrls: ['./test-case.component.scss']
})
@Injectable()
export class TestCaseComponent {
  @Input() testName!: string;
  @Input() staticSettings!: StaticSettings;
  @Input() iterations!: number
  @Output() testResults = new EventEmitter<ChartResult>();
  http: HttpClient;
  loading: boolean = false;

  constructor(private httpClient: HttpClient){
    this.http = httpClient
  }
  runTest(){
    this.loading = true
    console.log('starting', this.iterations)
    let dbs = ["mongodb", "postgresql"];
    let resultObservables: Observable<any>[] = []
    for(let db of dbs){
      let obs = this.http.get(this.staticSettings.url, {"params": {"iterations": this.iterations, "db": db}}).pipe(map(v => {return {db, v}}))
      resultObservables.push(obs)
    }

    forkJoin(resultObservables)
    .subscribe(r =>{
      console.log("test-case", r)
      let seriesArr = r.map(({db, v}) => prepareSeries(db, v))
      let chartResult: ChartResult = {
        data: seriesArr
      }
      this.testResults.emit(chartResult)
      this.loading = false
    })
    // this.runTestFun().subscribe((a) => {
    //   console.log(a)
    //   this.loading = false;
    // })

  }
}

function prepareSeries(db_name: string, data: SingleDbResult): ChartSeries{
  let data_points: DataPoint[] = data.times.map((el, idx) => {return {name: idx.toString(), value: el}})
  return { 
      name: db_name,
      series: data_points
    }
  }
