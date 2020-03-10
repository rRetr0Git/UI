<template>
  <div id="myCharts" ref="myCharts"></div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  mounted() {
      const  myCharts = this.$echarts.init(this.$refs.myCharts);
      let option = {
        color: ['#f44'],
        tooltip : {
          trigger: 'axis',
          axisPointer : {
            type : 'shadow'
          }
        },
        xAxis : [
          {
            type : 'category',
            data : ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月',],
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis : [
          {
            type : 'value'
          }
        ],
        series : [
          {
            name:'每月花费',
            type:'bar',
            barWidth: '60%',
            data:[995,666,444,858,654,236,645,546,846,225,547,356]
          }
        ]
      };
      myCharts.setOption(option);
      window.addEventListener('resize',function() {myChart.resize()});
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #myCharts{
    width: 100%;
    height: 800px;
    border: 1px solid red;
    margin: 0 auto;
  }
</style>
