export type StaticSettings = {
    url: string
}

export type TestCase = {
    name: string
    staticSettings: StaticSettings
}

export type SingleDbResult = {
    times: number[]
}

export type DataPoint = {
    name: string
    value: number
}

export type ChartSeries = {
    name: string
    series: DataPoint[]
}

export type ChartResult = {
   data: ChartSeries[] 
}