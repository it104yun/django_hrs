$(document).ready(function(){
   //echart---------------------------------------------------------------------------------------------------------begin
    var myChart = echarts.init(document.getElementById('main1'));

    // 指定图表的配置项和数据
    var option = {
        title: {
            text: 'ECharts示範'
        },
        tooltip: {},
        legend: {data:['技能成熟度(人數)'] },
        color: ['green'],
        xAxis: {
            data: ["不具備","生手級","新手級","半熟手級","導師級"]
        },
        yAxis: {},
        series: [{
            name: '技能成熟度(人數)',
            type: 'bar',
            data: [3,5, 20, 36, 10]
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

    // var myChart = echarts.init(document.getElementById('main2'));
        // var myChart = echarts.init(document.getElementById('main2'),'dark');       //(內置)預設
    var myChart = echarts.init(document.getElementById('main2'),'light');　　//(內置)預設
    // var myChart = echarts.init(document.getElementById('main2'),'wonderland');    //額外載入


    myChart.setOption({
          title: {
            text: 'ECharts示範',
            subtext: '成熟度比率',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
        color: ['#ff0000','#00ff00', '#0000ff', '#9FE6B8', '#FFDB5C','#ff9f7f', '#fb7293', '#E062AE', '#E690D1', '#e7bcf3', '#9d96f5', '#8378EA', '#96BFFF'],
        series : [
            {
                name: '成熟度比率',
                type: 'pie',    // 设置图表类型为饼图
                radius: '50%',  // 饼图的半径，外半径为可视区尺寸（容器高宽中较小一项）的 55% 长度。
                data:[          // 数据数组，name 为数据项名称，value 为数据项值
                    {value:4.05, name:'不具備'},
                    {value:6.76, name:'生手級'},
                    {value:27.03, name:'新手級'},
                    {value:36.00, name:'半熟手級'},
                    {value:13.51, name:'導師級'}
                ],
                emphasis: {
                    itemStyle: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
              }
            }
        ]
    })



    //echart--------------------------------------------------------------------------------------------------------ending


   //highchart---------------------------------------------------------------------------------------------------------begin
   //highchart----------------平面圓餅圖--示範1
    var chart = {
       plotBackgroundColor: null,
       plotBorderWidth: null,
       plotShadow: false
    };
   var title = { text: 'Highchart示範<br> 2022年 專業職能技能成熟度佔有比例' };

   var tooltip = { pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>' };

   var plotOptions = {
      pie: {
         allowPointSelect: true,
         cursor: 'pointer',
         dataLabels: {
            enabled: true,
            format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
            style: {
               color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
            }
         }
      }
   };

   var series= [{
      type: 'pie',
      name: '成熟度比率',
      data: [
         ['不具備',   4.05],
         ['生手級',   6.76],
         {
            name: '新手級',
            y: 27.03,
            sliced: true,
            selected: true
         },
         ['半熟手級',    36.00],
         ['導師級',     13.51],
      ]
   }];

   var json = {};
   json.chart = chart;
   json.title = title;
   json.tooltip = tooltip;
   json.series = series;
   json.plotOptions = plotOptions;
   $('#main3').highcharts(json);


   //highchart----------------3D圓餅圖--示範2
   var chart = {
      type: 'pie',
      options3d: {
         enabled: true,
         alpha: 45,
         beta: 0
      }
   };
   var title = { text: 'Highchart示範<br> 2022年 專業職能技能成熟度佔有比例'   };
   var tooltip = {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
   };

   var plotOptions = {
      pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          depth: 35,
          dataLabels: {
             enabled: true,
             // format: '{point.name}'
             format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
             style: {
               color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
            }
          }
      }
   };
   var series= [{
         type: 'pie',
            name: '成熟度比率',
            data: [
                ['不具備',  4.05],
                ['生手級',  6.76],
                {
                    name: '新手級',
                    y: 27.03,
                    sliced: true,
                    selected: true
                },
                ['半熟手級', 36.00],
                ['導師級',  13.51],
            ]
   }];

   var json = {};
   json.chart = chart;
   json.title = title;
   json.tooltip = tooltip;
   json.plotOptions = plotOptions;
   json.series = series;
   $('#main4').highcharts(json);
   //highchart---------------------------------------------------------------------------------------------------------ending


});