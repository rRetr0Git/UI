<template>
        <div id="myCharts" ref="myCharts"></div>
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
        $.ajaxSetup({async:false});
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
                  if(e.categories.toString()===(["CE"]).toString()) return;
                  if(e.categories.toString()===(["VPE"]).toString()) return;
                  let left = e.data.名称.lastIndexOf("\:")
                  let right = e.data.名称.lastIndexOf("\-")
                  let name = e.data.名称.substring(0,left)
                  barType.push(name)
                  geoCoordMap[name] = [parseFloat(e.geo.longitude),parseFloat(e.geo.latitude)]
                  fullName[name] = e.data.名称
                  status[name] = e.data.状态
                  categories[name] = e.categories[0]
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
                    title: {
                        subtext: ''
                    },

                    tooltip: {
                      trigger: 'item',
                      formatter:function (params) {
                          var res = '';
                          if(params.componentSubType==="lines") return;
                          res+=fullName[params['data'].name]+'</br>';
                          res+='状态:'+status[params['data'].name]+'</br>';
                          res+='类别:'+categories[params['data'].name]+'</br>';
                          return res;
                      }
                    },
                    calculable: true,
                    grid: {
                        top: 80,
                        bottom: 80,
                        right: '3%',
                        width: '20%'
                    },
                    geo: {
                        type: 'map',
                        mapType: 'shanghai',
                        roam: true,
                        top: "0%",

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
                        animation: false
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
                            if(e.target in partMap){
                                partMap[e.target].push({name:e.source})
                                partMapLink[e.target].push({source:e.source,target:e.target,lineStyle:{width: 5,curveness: 0.2}})
                            }
                            else{
                                partMap[e.target]=[]
                                partMap[e.target].push({name:e.source})
                                partMap[e.target].push({name:e.target})
                                partMapLink[e.target]=[]
                                partMapLink[e.target].push({source:e.source,target:e.target,lineStyle:{width: 5,curveness: 0.2}})
                            }
                          }
                          if(e.type==="VPE_PEA") return;
                          if(e.type==="CE_PEA") return;
                          if(e.type==="CE_VPE") return;
                          mapFlyLinesData.push([{
                              coord: geoCoordMap[e.source]
                          }, {
                              coord: geoCoordMap[e.target]
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
                                symbolSize: 3, //图标大小
                            },
                            lineStyle: {
                                normal: {
                                    color: colorType[i],
                                    width: 0.3, //尾迹线条宽度
                                    opacity: 0.5, //尾迹线条透明度
                                    curveness: .1 //尾迹线条曲直度
                                }
                            },
                            data: mapFlyLinesData
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
                if(params.componentSubType=='effectScatter'){
                    console.log(partMap[params.data.name])
                    console.log(partMapLink[params.data.name])
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
                                icon: 'path://M432.45,595.444c0,2.177-4.661,6.82-11.305,6.82c-6.475,0-11.306-4.567-11.306-6.82s4.852-6.812,11.306-6.812C427.841,588.632,432.452,593.191,432.45,595.444L432.45,595.444z M421.155,589.876c-3.009,0-5.448,2.495-5.448,5.572s2.439,5.572,5.448,5.572c3.01,0,5.449-2.495,5.449-5.572C426.604,592.371,424.165,589.876,421.155,589.876L421.155,589.876z M421.146,591.891c-1.916,0-3.47,1.589-3.47,3.549c0,1.959,1.554,3.548,3.47,3.548s3.469-1.589,3.469-3.548C424.614,593.479,423.062,591.891,421.146,591.891L421.146,591.891zM421.146,591.891',
                                onclick: function (){
                                    location.reload();
                                }
                            }
                        }
                      },
                      title: {
                          text: 'Graph 简单示例'
                      },
                      animationDurationUpdate: 1500,
                      animationEasingUpdate: 'quinticInOut',
                      series: [
                          {
                              type: 'graph',
                              layout: 'circular',
                              symbolSize: 50,
                              roam: true,
                              label: {
                                  show: true
                              },
                              edgeSymbol: ['circle', 'arrow'],
                              edgeSymbolSize: [4, 10],
                              edgeLabel: {
                                  fontSize: 20
                              },
                              data: partMap[params.data.name],
                              links: partMapLink[params.data.name],
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
    height: 900px;
    margin: 0 auto;
  }

</style>
