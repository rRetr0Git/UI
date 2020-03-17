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
        $.getJSON(uploadedDataURL, function(geoJson) {
            _this.$echarts.registerMap('', geoJson); //注册 地图

            // 各区中心点经纬度
            var geoCoordMap = {};

            // 柱状图纵坐标
            var barType = []
            var excludeCity = ["茂名市", "阳江市", "湛江市", "揭阳市", "梅州市", "潮州市", "汕头市", "汕尾市"]
            var geoData = JSON.parse(JSON.stringify(geoJson))
            geoData.features.forEach(e => {
                if(excludeCity.includes(e.properties.name)) return;
                barType.push(e.properties.name)
                geoCoordMap[e.properties.name] = e.properties.cp
            })
            barType=["1-P-DXC:10.1.1.1 - 深圳", "1-P-GZ:10.1.1.21 - 广州", "1-P-SG:10.1.1.31 - 韶关"]
            geoCoordMap={"1-P-DXC:10.1.1.1 - 深圳": [114.057868, 22.543099], "1-P-GZ:10.1.1.21 - 广州": [113.264434, 23.129162], "1-P-SG:10.1.1.31 - 韶关": [113.597522, 24.810403]}
            // 数据梯度或类别
            var dataType = ["总览", "节点信息", "通路信息", "特殊信息"]
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
                        left: "10%",
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
                    var value = _random(100, 800);
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

                    var endPoint = barType[_random(0, barType.length - 1)]

                    if (endPoint === res) return;
                    mapFlyLinesData.push([{
                        coord: geoCoordMap[res]
                    }, {
                        coord: geoCoordMap[endPoint]
                    }])
                })

                // change options
                option.options.push({
                    title: [{
                        id: 'title1',
                        text: e + "统计",
                        right: '10%',
                        top: '2%',
                        textStyle: {
                            color: '#fff',
                            fontSize: 12
                        }
                    }],
                    xAxis: {
                        type: 'value',
                        scale: true,
                        position: 'top',
                        min: 0,
                        boundaryGap: false,
                        splitLine: {
                            show: false
                        },
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        axisLabel: {
                            margin: 2,
                            textStyle: {
                                color: '#aaa'
                            }
                        },
                    },
                    yAxis: {
                        type: 'category',
                        nameGap: 16,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: '#ddd'
                            }
                        },
                        axisTick: {
                            show: false,
                            lineStyle: {
                                color: '#ddd'
                            }
                        },
                        axisLabel: {
                            interval: 0,
                            textStyle: {
                                color: '#ddd'
                            }
                        },
                        data: barType
                    },
                    series: [
                        // scatter 数据映射
                        {
                            name: 'point',
                            type: 'scatter',
                            coordinateSystem: 'geo',
                            data: mapData,
                            symbolSize: function(val) {
                                return val[2] / 30;
                            },
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
                            symbolSize: function(val) {
                                return val[2] / 30;
                            },
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
                        },
                        //柱状图
                        {
                            zlevel: 1.5,
                            type: 'bar',
                            symbol: 'none',
                            itemStyle: {
                                normal: {
                                    color: colorType[i],
                                    label: {
                                        show: true,
                                        position: 'right',
                                        textStyle: {
                                            color: 'white'
                                        }
                                    }
                                }
                            },
                            data: barData
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
