const JSONHistory = require('./JSONHistory.js')
import vegaEmbed from 'vega-embed'

let setStats = (history) => {
    history = JSONHistory.convertHistoryToJSON(history)
    let barChart = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "description": "A simple bar chart with embedded data.",
        "title": "Average Opioid Sale and Thefts By Year",
        "width": 800,
        "height": 550,
        "data": {
            "values": history
        },
        "mark": "bar",
        "encoding": {
            "x": {
                "bin": true,
                "field": "time_stamp",
                "type": "temporal"
            },
            "y": {
                "aggregate": "count",
                "type": "quantitative"
            }
        }
    }
    vegaEmbed('#chart', barChart)
}




export {
    setStats
}
