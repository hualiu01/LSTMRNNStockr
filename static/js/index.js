// var chart = AmCharts.makeChart( "chartdiv", {
function draw_hist_chart(hist_url) {
  AmCharts.makeChart( "chartdiv", {
    "type": "stock",
    "theme": "none",

    //"color": "#fff",
    "dataSets": [ {
      "title": "MSFT",
      "fieldMappings": [ {
        "fromField": "Open",
        "toField": "open"
      }, {
        "fromField": "High",
        "toField": "high"
      }, {
        "fromField": "Low",
        "toField": "low"
      }, {
        "fromField": "Close",
        "toField": "close"
      }, {
        "fromField": "Volume",
        "toField": "volume"
      } ],
      "compared": false,
      "categoryField": "Date",

      /**
       * data loader for data set data
       */
      "dataLoader": {
        "url": hist_url,
        "format": "csv",
        "showCurtain": true,
        "showErrors": true,
        "async": true,
        "reverse": true,
        "delimiter": ",",
        "useColumnNames": true
      },

      /**
       * data loader for events data
       */
      // "eventDataLoader": {
      //   "url": "https://www.amcharts.com/wp-content/uploads/assets/stock/MSFT_events.csv",
      //   "format": "csv",
      //   "showCurtain": true,
      //   "showErrors": true,
      //   "async": true,
      //   "reverse": true,
      //   "delimiter": ",",
      //   "useColumnNames": true,
      //   "postProcess": function( data ) {
      //     for ( var x in data ) {
      //       switch ( data[ x ].Type ) {
      //         case 'A':
      //           var color = "#85CDE6";
      //           break;
      //         default:
      //           var color = "#cccccc";
      //           break;
      //       }
      //       data[ x ].Description = data[ x ].Description.replace( "Upgrade", "<strong style=\"color: #0c0\">Upgrade</strong>" ).replace( "Downgrade", "<strong style=\"color: #c00\">Downgrade</strong>" );
      //       data[ x ] = {
      //         "type": "pin",
      //         "graph": "g1",
      //         "backgroundColor": color,
      //         "date": data[ x ].Date,
      //         "text": data[ x ].Type,
      //         "description": "<strong>" + data[ x ].Title + "</strong><br />" + data[ x ].Description
      //       };
      //     }
      //     return data;
      //   }
      // }

    }, 
    // {
    //   "title": "TXN",
    //   "fieldMappings": [ {
    //     "fromField": "Open",
    //     "toField": "open"
    //   }, {
    //     "fromField": "High",
    //     "toField": "high"
    //   }, {
    //     "fromField": "Low",
    //     "toField": "low"
    //   }, {
    //     "fromField": "Close",
    //     "toField": "close"
    //   }, {
    //     "fromField": "Volume",
    //     "toField": "volume"
    //   } ],
    //   "compared": true,
    //   "categoryField": "Date",
    //   "dataLoader": {
    //     "url": "https://www.amcharts.com/wp-content/uploads/assets/stock/TXN.csv",
    //     "format": "csv",
    //     "showCurtain": true,
    //     "showErrors": true,
    //     "async": true,
    //     "reverse": true,
    //     "delimiter": ",",
    //     "useColumnNames": true
    //   }
    // } 
    ],
    "dataDateFormat": "YYYY-MM-DD",

    "panels": [ {
        "title": "Value",
        "percentHeight": 70,

        "stockGraphs": [ {
          "type": "candlestick",
          "id": "g1",
          "openField": "open",
          "closeField": "close",
          "highField": "high",
          "lowField": "low",
          "valueField": "close",
          "lineColor": "#fff",
          "fillColors": "#fff",
          "negativeLineColor": "#db4c3c",
          "negativeFillColors": "#db4c3c",
          "fillAlphas": 1,
          "comparedGraphLineThickness": 2,
          "columnWidth": 0.7,
          "useDataSetColors": false,
          "comparable": true,
          "compareField": "close",
          "showBalloon": false,
          "proCandlesticks": true
        } ],

        "stockLegend": {
          "valueTextRegular": undefined,
          "periodValueTextComparing": "[[percents.value.close]]%"
        }

      },

      {
        "title": "Volume",
        "percentHeight": 30,
        "marginTop": 1,
        "columnWidth": 0.6,
        "showCategoryAxis": false,

        "stockGraphs": [ {
          "valueField": "volume",
          "openField": "open",
          "type": "column",
          "showBalloon": false,
          "fillAlphas": 1,
          "lineColor": "#fff",
          "fillColors": "#fff",
          "negativeLineColor": "#db4c3c",
          "negativeFillColors": "#db4c3c",
          "useDataSetColors": false
        } ],

        "stockLegend": {
          "markerType": "none",
          "markerSize": 0,
          "labelText": "",
          "periodValueTextRegular": "[[value.close]]"
        },

        "valueAxes": [ {
          "usePrefixes": true
        } ]
      }
    ],

    "panelsSettings": {
      //    "color": "#fff",
      "plotAreaFillColors": "#333",
      "plotAreaFillAlphas": 1,
      "marginLeft": 60,
      "marginTop": 5,
      "marginBottom": 5
    },

    "chartScrollbarSettings": {
      "graph": "g1",
      "graphType": "line",
      "usePeriod": "WW",
      "backgroundColor": "#333",
      "graphFillColor": "#666",
      "graphFillAlpha": 0.5,
      "gridColor": "#555",
      "gridAlpha": 1,
      "selectedBackgroundColor": "#444",
      "selectedGraphFillAlpha": 1
    },

    "categoryAxesSettings": {
      "equalSpacing": true,
      "gridColor": "#555",
      "gridAlpha": 1
    },

    "valueAxesSettings": {
      "gridColor": "#555",
      "gridAlpha": 1,
      "inside": false,
      "showLastLabel": true
    },

    "chartCursorSettings": {
      "pan": true,
      "valueLineEnabled": true,
      "valueLineBalloonEnabled": true
    },

    "legendSettings": {
      //"color": "#fff"
    },

    "stockEventsSettings": {
      "showAt": "high",
      "type": "pin"
    },

    "balloon": {
      "textAlign": "left",
      "offsetY": 10
    },

    "periodSelector": {
      "position": "bottom",
      "periods": [ {
          "period": "DD",
          "count": 10,
          "label": "10D"
        }, {
          "period": "MM",
          "count": 1,
          "label": "1M"
        }, {
          "period": "MM",
          "count": 6,
          "label": "6M"
        }, {
          "period": "YYYY",
          "count": 1,
          "label": "1Y"
        },
        /* {
             "period": "YTD",
             "label": "YTD"
           },*/
        {
          "period": "MAX",
          "label": "MAX"
        }
      ]
    }
  });
}

String.prototype.format = function () {
        var args = [].slice.call(arguments);
        return this.replace(/(\{\d+\})/g, function (a){
            return args[+(a.substr(1,a.length-2))||0];
        });
};

$("#stock_search_btn").on("click", function(){
  // hist_url = "https://www.amcharts.com/wp-content/uploads/assets/stock/MSFT.csv";
  hist_url = "/static/data/{0}.csv".format(symbol);
  draw_hist_chart(hist_url);
});

$(document).ready(function(){
  // hist_url = "https://www.google.com/finance/historical?output=csv&q=aapl";
  hist_url = "/static/data/{0}.csv".format(symbol);
  console.log(symbol)
  draw_hist_chart(hist_url);
});


