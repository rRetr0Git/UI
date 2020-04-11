<template>
    <div>
        <div id="myCharts" ref="myCharts"></div>
    </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  mounted(){
        const  myCharts = this.$echarts.init(this.$refs.myCharts,'dark');

        // 指定图表的配置项和数据
        var uploadedDataURL = "../static/json/data-1482909784051-BJgwuy-Sl.json";
        var _this = this

        var seriesLabel = {
            normal: {
                show: true,
                textBorderColor: '#ccc',
                textBorderWidth: 2
            }
        };

        $.ajaxSetup({async:false});

        var countInfoUrl = "../static/testApi/overview.json";
        var overviewData = {}
        $.getJSON(countInfoUrl, function(count) {
            var countData = JSON.parse(JSON.stringify(count))
            overviewData.cpeCount = countData['cpeCount']
            overviewData.vpeCount = countData['vpeCount']
            overviewData.peCount = countData['peCount']
            overviewData.popCount = countData['popCount']
            overviewData.tenantCount = countData['tenantCount']
        })

        var topTenInfoUrl = "../static/testApi/top_10_if.json";
        var topTenRxData = {host:[],ifname:[],usage:[]}
        var topTenTxData = {host:[],ifname:[],usage:[]}
        $.getJSON(topTenInfoUrl, function(topTen) {
            var topTenData = JSON.parse(JSON.stringify(topTen))
            topTenData.rx.forEach(e => {
                topTenRxData.host.push(e.host)
                topTenRxData.ifname.push(e.ifname)
                topTenRxData.usage.push(e.usage)
            })

            topTenData.tx.forEach(e => {
                topTenTxData.host.push(e.host)
                topTenTxData.ifname.push(e.ifname)
                topTenTxData.usage.push(e.usage)
            })
        })

        var peInfoUrl = "../static/testApi/pe.json";
        var peAllData = {}
        $.getJSON(peInfoUrl, function(pe) {
            var peData = JSON.parse(JSON.stringify(pe))
            pe.forEach(e => {
                peAllData[e.name] = e
            })
        })

        var peInterfaceInfoUrl = "../static/testApi/pe_interface_stats.json";
        var peInterfaceAllData = {}
        $.getJSON(peInterfaceInfoUrl, function(peInterface) {
            var peInterfaceData = JSON.parse(JSON.stringify(peInterface))
            peInterface.forEach(e => {
                if(e.host in peInterfaceAllData){
                    peInterfaceAllData[e.host].push(e)
                }
                else{
                    peInterfaceAllData[e.host] = []
                    peInterfaceAllData[e.host].push(e)
                }
            })
        })

        console.log(peInterfaceAllData)

        var edgeInfo = []
        $.getJSON(uploadedDataURL, function(geoJson) {
            _this.$echarts.registerMap('', geoJson); //注册 地图

            // 各区中心点经纬度
            var geoCoordMap = {}
            var fullName = {}
            var status = {}
            var categories = {}
            // 柱状图纵坐标
            var barType = []
            var partMap = {}
            var partMapLink = {}
            var geoInfoUrl = "../static/testApi/graph.json";
            $.getJSON(geoInfoUrl, function(geo) {
              var geoData = JSON.parse(JSON.stringify(geo))
              geoData.visualization.nodes.forEach(e => {
                  let left = e.data.名称.lastIndexOf("\:")
                  let right = e.data.名称.lastIndexOf("\-")
                  let name = e.data.名称.substring(0,left)

                  fullName[name] = e.data.名称
                  status[name] = e.data.状态
                  categories[name] = e.categories[0]
                  if(e.categories.toString()===(["CE"]).toString()) return;
                  if(e.categories.toString()===(["VPE"]).toString()) return;
                  barType.push(name)
                  geoCoordMap[name] = [parseFloat(e.geo.longitude),parseFloat(e.geo.latitude)]
              })
            })
            // 数据梯度或类别
            var dataType = ["总览"]
            var colorType = ['#00ffea', '#00ff8c', '#f9ff00', '#ff5500']

            var option = {
                // 时间轴样式
                backgroundColor: '#2c343c',
                baseOption: {
                    timeline: {
                        axisType: 'category',
                        autoPlay: true,
                        playInterval: 10000,
                        data: dataType,
                        label: {
                            color: 'rgba(0,168,255,.6)'
                        },
                        lineStyle: {
                            color: '#666'
                        },
                        checkpointStyle: {
                            color: 'rgba(0,168,255,1)',
                            borderColor: 'rgba(0,168,255,0.3)'
                        },
                        itemStyle: {
                            opacity: 0.3
                        },
                        controlStyle: {
                            opacity: 0.3
                        },
                        emphasis: {
                            label: {
                                color: 'rgba(0,168,255,1)'
                            },
                            controlStyle: {
                                color: 'rgba(0,168,255,1)',
                                borderColor: 'rgba(0,168,255,1)',
                                opacity: 1
                            }
                        }
                    },
                    title: [
                        {
                            text:'Overview',
                            left:'12%',
                            top:'3%',
                        }
                    ],
                    xAxis: [{
                        type: 'value',
                        name: 'Number',
                        axisLabel: {
                            formatter: '{value}'
                        }
                    },{
                        gridIndex:1,
                        type: 'value',
                        name: 'Number',
                        axisLabel: {
                            formatter: '{value}'
                        }
                    }],
                    yAxis: [{
                        type: 'category',
                        name: 'Category',
                        inverse: true,
                        data: ['Tenant', 'POP', 'CPE','VPE','PE'],
                        axisLabel: {
                            margin: 20,
                        }
                    },{
                        gridIndex: 1,
                        type: 'category',
                        name: 'Name',
                        data: ['Top1','Top2','Top3','Top4','Top5','Top6','Top7','Top8','Top9','Top10'],
                        inverse: true,
                        axisLabel: {
                            interval: 0,
                            rotate: 30
                        },
                        splitLine: {
                            show: false
                        }
                    }],
                    legend:{
                        top:'50%',
                        left:'8%',
                        data:['RX','TX']
                    },
                    tooltip: {
                      trigger: 'item',
                      enterable:true,
                      formatter:function (params) {
                          var res = '';
                          if(params.componentSubType==="graph") return;

                          if(params.componentSubType==="bar"&&params.componentIndex===3){
                            res+=params.name+'数:'+params.data+'</br>';
                            return res;
                          }
                          if(params.componentSubType==="bar"&&params.componentIndex==4){
                            res+=topTenRxData.host[params.dataIndex]+'</br>';
                            res+=topTenRxData.ifname[params.dataIndex]+'</br>';
                            res+=topTenRxData.usage[params.dataIndex]+'</br>';
                            return res;
                          }
                          if(params.componentSubType==="bar"&&params.componentIndex==5){
                            res+=topTenTxData.host[params.dataIndex]+'</br>';
                            res+=topTenTxData.ifname[params.dataIndex]+'</br>';
                            res+=topTenTxData.usage[params.dataIndex]+'</br>';
                            return res;
                          }
                          return res;
                      }
                    },
                    calculable: true,
                    grid: [{
                          x:"5%",
                          top: '10%',
                          bottom: 80,
                          right: '3%',
                          height: "25%",
                          width: '15%'
                    },{
                          x:"5%",
                          top: '55%',
                          bottom: 80,
                          right: '3%',
                          height: "35%",
                          width: '15%'
                    }],
                    geo: {
                        type: 'map',
                        mapType: 'guangdong',
                        roam: false,
                        top: "0%",
                        left: "22%",
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: false,
                                textStyle: {
                                    color: '#000'
                                }
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderColor: 'rgba(0,168,255,.6)',
                                borderWidth: 2,
                                areaColor: 'rgba(0,81,138,.3)',
                            },
                            emphasis: {
                                borderColor: 'rgba(0,168,255,.6)',
                                borderWidth: 2,
                                areaColor: 'rgba(0,81,138,.3)',
                            }
                        },
                        animation: false,
                        tooltip: {
                          trigger: 'item',
                          enterable:true,
                          position:['75%','5%'],
                          textStyle:{
                            fontSize:14,
                          },
                          hideDelay:100000,
                          borderColor:'#ffffff',
                          borderWidth:'2',
                          formatter:function (params) {
                              var upMarker='<span style=\"display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#00ff00;\"></span>'
                              var downMarker='<span style=\"display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#ff0000;\"></span>'
                              var res = '';
                              if(params.componentSubType==='effectScatter'){
                                res+=params.marker+peAllData[params['data'].name].name+'</br><table>';
                                res+='<tr><td>City</td><td>'+peAllData[params['data'].name].city+'</td></tr>';
                                res+='<tr><td>Status</td><td>'+status[params['data'].name]+'</td></tr>';
                                res+='<tr><td>Categories</td><td>'+categories[params['data'].name]+'</td></tr>';
                                res+='<tr><td>ManageIp</td><td>'+peAllData[params['data'].name].manageIp+'</td></tr>';
                                res+='<tr><td>Number of Interface</td><td>'+peAllData[params['data'].name].peInterfaces.length+'</td></tr>';
                                var interfaces={}
                                for(var i=0;i<peAllData[params['data'].name].peInterfaces.length;i++){
                                  interfaces[peAllData[params['data'].name].peInterfaces[i].name] = peAllData[params['data'].name].peInterfaces[i].operStatus
                                }
                                var newData = {};
                                Object.keys(interfaces).sort().map(key => {
                                  newData[key]=interfaces[key]
                                })

                                let rx_bps = null
                                let tx_bps = null
                                for(let key in newData){
                                  if(params['data'].name in peInterfaceAllData){
                                    for(let i = 0; i < peInterfaceAllData[params['data'].name].length; i++){
                                      if(peInterfaceAllData[params['data'].name][i].ifname === key){
                                        rx_bps = parseInt(peInterfaceAllData[params['data'].name][i].rx_bps)
                                        tx_bps = parseInt(peInterfaceAllData[params['data'].name][i].tx_bps)
                                      }
                                    }
                                  }

                                  res+='<tr><td>'+key+'</td><td>'
                                  if(newData[key]==='UP'){
                                    res+=upMarker+newData[key]+'</td><td>'+ rx_bps + '</td><td>'+ tx_bps +'</td></tr>'
                                  }
                                  else{
                                    res+=downMarker+newData[key]+'</td><td>'+ rx_bps + '</td><td>'+ tx_bps +'</td></tr>'
                                  }
                                }
                                res+= '</table>'
                                if(params.componentSubType==='effectScatter'){
                                  if(params.data.name in partMap){
                                      res+='点击查看下层拓扑'+'</br>';
                                  }

                                }
                              }
                              if(params.componentSubType==="lines"){
                                 res+='<table>';
                                 res+='<tr><td>Source</td><td>'+edgeInfo[params.dataIndex].source+'</td></tr>';
                                 res+='<tr><td>Target</td><td>'+edgeInfo[params.dataIndex].target+'</td></tr>';
                                 res+='<tr><td>Status</td><td>'+edgeInfo[params.dataIndex].properties.链路状态+'</td></tr>';
                                 res+='<tr><td>Lag</td><td>'+edgeInfo[params.dataIndex].properties.延迟+'</td></tr>';
                                 res+='<tr><td>Loss</td><td>'+edgeInfo[params.dataIndex].properties.丢包+'</td></tr>';
                                 res+='<tr><td>S-Interface</td><td>'+edgeInfo[params.dataIndex].properties.源端口+'</td></tr>';
                                 res+='<tr><td>T-Interface</td><td>'+edgeInfo[params.dataIndex].properties.目的端口+'</td></tr>';
                                 res+='<tr><td>Bandwidth</td><td>'+'<span style=\"display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:'+params.color+';\"></span>'+edgeInfo[params.dataIndex].properties.当前带宽+'</td></tr>';
                                 res+='</table>';
                              }
                              return res;
                          }
                        },
                    }
                },
                options: []
            }

            dataType.forEach((e, i) => {
                // 柱状图模拟数据
                var barData = [];
                // 地图撒点数据 [{name:名字,value:[lng,lat,数值]}]
                var mapData = []
                // 地图飞线数据
                var mapFlyLinesData = [];

                barType.forEach(res => {
                    var value = _random(400, 800);
                    barData.push({
                        'name': res,
                        'value': value
                    })

                    var point = JSON.parse(JSON.stringify(geoCoordMap[res]));
                    point.push(value)
                    mapData.push({
                        'name': res,
                        'value': point
                    })
                })

                $.getJSON(geoInfoUrl, function(geo) {
                      var geoData = JSON.parse(JSON.stringify(geo))
                      geoData.visualization.edges.forEach(e => {
                          if(e.type==="PEB_PEB" || e.type=='PEA_PEB'){}
                          else{
                            var source = ''
                            if(e.target in partMap){
                                if(e.source.length>16){
                                  geoData.visualization.nodes.forEach(f=>{
                                    if(e.source === f.id){
                                      source = f.data.名称
                                    }
                                  })
                                }
                                else{
                                  source = e.source
                                }
                                partMap[e.target].push({name:source,itemStyle:{color: '#00ffea'}})
                                partMapLink[e.target].push({source:source,target:e.target,lineStyle:{width: 3,curveness: 0.2,type:'dotted',color:'#00ffea'}})
                            }
                            else{
                                if(e.source.length>16){
                                  geoData.visualization.nodes.forEach(f=>{
                                    if(e.source === f.id){
                                      source = f.data.名称
                                    }
                                  })
                                }
                                else{
                                  source = e.source
                                }
                                partMap[e.target]=[]
                                partMap[e.target].push({name:source,itemStyle:{color: '#00ffea'}})
                                partMap[e.target].push({name:e.target,itemStyle:{color: '#00ffea'}})
                                partMapLink[e.target]=[]
                                partMapLink[e.target].push({source:source,target:e.target,lineStyle:{width: 3,curveness: 0.2,type:'dotted',color:'#00ffea'}})
                            }
                          }
                          if(e.type==="VPE_PEA") return;
                          if(e.type==="CE_PEA") return;
                          if(e.type==="CE_VPE") return;

                          var colorStop='#00ff8c'

                          if(e.properties.当前带宽>5000){
                              colorStop='#00ffea'
                          }

                          if(e.properties.当前带宽>10000){
                              colorStop='#f9ff00'
                          }


                          if(e.properties.链路状态==='DOWN'){
                              colorStop='#ff5500'
                          }
                          edgeInfo.push(e)
                          mapFlyLinesData.push([{
                              coord: geoCoordMap[e.source],
                              lineStyle:{
                                  color:colorStop,
                              }
                          },{
                              coord: geoCoordMap[e.target],
                          }])
                      })
                })


                // change options
                option.options.push({

                    series: [
                        // scatter 数据映射
                        {
                            name: 'point',
                            type: 'scatter',
                            coordinateSystem: 'geo',
                            data: mapData,
                            symbolSize: 20,
                            itemStyle: {
                                normal: {
                                    color: colorType[i]
                                }
                            }
                        },
                        // effectScatter 点位动画 数据映射  此层覆盖掉scatter层 若想看上一层可把此obj注销 或提高上一层的层级
                        {
                            type: 'effectScatter',
                            coordinateSystem: 'geo',
                            data: mapData,
                            symbolSize: 20,
                            showEffectOn: 'render',
                            rippleEffect: {
                                brushType: 'stroke'
                            },
                            hoverAnimation: true,
                            label: {
                                normal: {
                                    formatter: '{b}',
                                    position: 'right',
                                    show: true
                                }
                            },
                            itemStyle: {
                                normal: {
                                    color: colorType[i],
                                    shadowBlur: 10,
                                    shadowColor: colorType[i]
                                }
                            },
                            zlevel: 1
                        },
                        //飞线层
                        {
                            type: 'lines',
                            zlevel: 2,
                            effect: {
                                show: true,
                                period: 4, //箭头指向速度，值越小速度越快
                                trailLength: 0.02, //特效尾迹长度[0,1]值越大，尾迹越长重
                                symbol: 'arrow', //箭头图标
                                symbolSize: 5, //图标大小
                            },
                            lineStyle: {
                                normal: {
                                    color: colorType[i],
                                    width: 2, //尾迹线条宽度
                                    opacity: 0.5, //尾迹线条透明度
                                    curveness: .1 //尾迹线条曲直度
                                }
                            },
                            data: mapFlyLinesData,

                        },
                        {
                            xAxisIndex:0,
                            yAxisIndex:0,
                            type: 'bar',
                            data: [overviewData.tenantCount,overviewData.popCount,overviewData.cpeCount,overviewData.vpeCount,overviewData.peCount],
                            label: seriesLabel
                        },
                        {
                            name:'RX',
                            xAxisIndex:1,
                            yAxisIndex:1,
                            type: 'bar',
                            data: topTenRxData.usage,
                        },
                        {
                            name:'TX',
                            xAxisIndex:1,
                            yAxisIndex:1,
                            type: 'bar',
                            data: topTenTxData.usage,
                        },
                        {
                            name: 'Alert',
                            type: 'pie',
                            radius: '30%',
                            center: ['85%', '75%'],
                            data: [
                                {value: 4, name: '链路通路'},
                                {value: 2, name: 'API下发失败'},
                                {value: 2.5, name: 'Alert Type-1'},
                                {value: 3.5, name: 'Alert Type-2'},
                                {value: 3, name: 'Alert Type-3'},
                            ].sort(function (a, b) { return a.value - b.value; }),
                            roseType: 'radius',
                            label: {
                                color: 'rgba(255, 255, 255)'
                            },
                            tooltip: {
                                trigger: 'item',
                                formatter: '{a} <br/>{b} : {c} ({d}%)'
                            },
                            labelLine: {
                                lineStyle: {
                                    color: 'rgba(255, 255, 255)'
                                },
                                smooth: 0.2,
                                length: 10,
                                length2: 20
                            },
                            itemStyle: {
                                color: '#A7B4DE',
                                shadowBlur: 200,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            },

                            animationType: 'scale',
                            animationEasing: 'elasticOut',
                            animationDelay: function (idx) {
                                return Math.random() * 200;
                            }
                        }
                    ]
                })
            })


            myCharts.setOption(option)

            window.onresize = function(){
                myCharts.resize();
            }

            myCharts.on('click', function (params) {
                console.log(params);
                if(params.componentSubType=='effectScatter'&&params.data.name in partMap){
                    let option={
                      color: ['#f44'],
                      tooltip : {
                        trigger: 'axis',
                        axisPointer : {
                          type : 'shadow'
                        }
                      },
                      //
                      toolbox: {
                        itemSize:50,
                        left:200,
                        top:50,
                        feature: {
                            myTool1: {
                                show: true,
                                title: 'Return',
                                icon: 'image://../static/return.png',
                                onclick: function (){
                                    location.reload();
                                }
                            }
                        }
                      },
                      title: {

                      },
                      animationDurationUpdate: 1500,
                      animationEasingUpdate: 'quinticInOut',
                      series: [
                          {
                              type: 'graph',
                              layout: 'circular',
                              symbolSize: 50,
                              roam: false,
                              label: {
                                  show: true,
                                  position:'top',
                                  fontStyle:'oblique'
                              },
                              edgeSymbol: ['circle', 'arrow'],
                              edgeSymbolSize: [4, 10],
                              edgeLabel: {
                                  fontSize: 20
                              },
                              data: partMap[params.data.name],
                              links: partMapLink[params.data.name],
                              tooltip: {
                                trigger: 'item',
                                enterable:true,
                                position:['80%','5%'],
                                textStyle:{
                                  fontSize:16,
                                },
                                borderColor:'#ffffff',
                                borderWidth:'2',
                                formatter:function (params) {
                                    var upMarker='<span style=\"display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#00ff00;\"></span>'
                                    var downMarker='<span style=\"display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:#ff0000;\"></span>'
                                    var res = '';
                                    if(params.componentSubType==='graph' && params.dataType==='node'){
                                      if(params['data'].name in peAllData){
                                        res+=params.marker+peAllData[params['data'].name].name+'</br><table>';
                                        res+='<tr><td>City</td><td>'+peAllData[params['data'].name].city+'</td></tr>';
                                        res+='<tr><td>Status</td><td>'+status[params['data'].name]+'</td></tr>';
                                        res+='<tr><td>Categories</td><td>'+categories[params['data'].name]+'</td></tr>';
                                        res+='<tr><td>ManageIp</td><td>'+peAllData[params['data'].name].manageIp+'</td></tr>';
                                        res+='<tr><td>Number of Interface</td><td>'+peAllData[params['data'].name].peInterfaces.length+'</td></tr>';
                                        var interfaces={}
                                        for(var i=0;i<peAllData[params['data'].name].peInterfaces.length;i++){
                                          interfaces[peAllData[params['data'].name].peInterfaces[i].name] = peAllData[params['data'].name].peInterfaces[i].operStatus
                                        }
                                        var newData = {};
                                        Object.keys(interfaces).sort().map(key => {
                                          newData[key]=interfaces[key]
                                        })
                                        for(let key in newData){
                                          res+='<tr><td>'+key+'</td><td>'
                                          if(newData[key]==='UP'){
                                            res+=upMarker+newData[key]+'</td></tr>'
                                          }
                                          else{
                                            res+=downMarker+newData[key]+'</td></tr>'
                                          }
                                        }
                                        res+= '</table>'
                                      }
                                    }
                                    return res;
                                }
                              },
                          }
                      ],
                      lineStyle: {
                          color: 'source',
                          curveness: 2
                      }
                    }
                    myCharts.resize();
                    myCharts.setOption(option,{notMerge:true,lazyUpdate:false});
                }
                else{
                    console.log('make it deep')
                }
            });
        })
        function _random(a, b) {
            return Math.round(Math.random() * Math.abs(b - a) + a)
        }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

  #myCharts{
    width: 100%;
    height:900px;
    margin: 0 auto;
  }

</style>
