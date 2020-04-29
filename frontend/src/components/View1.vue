
<template>
  <div>
    <el-table
      :data="tenantAllData"
      height="900"
      border
      stripe
      style="width: 100%">
      <el-table-column
        prop="dst"
        sortable
        label="DST">
      </el-table-column>
      <el-table-column
        prop="src"
        sortable
        label="SRC">
      </el-table-column>
      <el-table-column
        prop="tun"
        sortable
        label="TUN">
        <template slot-scope="scope">
          <el-button type="primary" plain size="medium" @click="checkTun(scope.$index, scope.row)"><i class="el-icon-view el-icon--right"></i>  {{ scope.row.tun }}</el-button>
        </template>
      </el-table-column>
      <el-table-column
        prop="vrf"
        sortable
        label="VRF">
      </el-table-column>
      <el-table-column
        prop="bps"
        sortable
        label="BPS">
      </el-table-column>
      <el-table-column
        prop="pps"
        sortable
        label="PPS">
      </el-table-column>
    </el-table>
    <el-dialog
      title="Details"
      @opened="open()"
      :visible.sync="dialogVisible"
      width="80%"
      :before-close="handleClose">
      <div id="myCharts" ref="myCharts"></div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import $ from 'jquery'
import 'jquery/dist/jquery.js'
import 'bootstrap-table/dist/bootstrap-table.js'
import 'bootstrap-table/dist/bootstrap-table.css'
import 'bootstrap/dist/css/bootstrap-table-fixed-columns.css'
import 'bootstrap/dist/js/bootstrap-table-fixed-columns.js'

var tenantAllData =[]
var teAllData = []
var tePathAllData = []
var teVisData = {}
var teVisLinks = {}
$.ajaxSetup({async:false});

/*
var tenantInfoUrl = "../../static/testApi/tenant_te_traffic.json";
var teInfoUrl = "../../static/testApi/te_if_state.json";
var tePathInfoUrl = "../../static/testApi/te_1.json";

$.getJSON(tenantInfoUrl, function(tenant) {
  var tenantData = JSON.parse(JSON.stringify(tenant))
  tenantData.result.forEach(e => {
    tenantAllData.push(e)
  })
})

$.getJSON(teInfoUrl, function(te) {
  var teData = JSON.parse(JSON.stringify(te))
  teData.forEach(e => {
    teAllData.push(e)
  })
})

$.getJSON(tePathInfoUrl, function(tePath) {
  var tePathData = JSON.parse(JSON.stringify(tePath))
  tePathData.results.item.forEach(e => {
    tePathAllData.push(e)
    teVisData[e.name] = []
    teVisData[e.name].push({name:e.srcPe,symbolSize:40})
    teVisLinks[e.name] = []
    var tempSrc = e.srcPe
    e.teTunnelPaths[0].paths.forEach(f => {
      teVisData[e.name].push({name:f.peId,symbolSize:40})
      teVisLinks[e.name].push({source:tempSrc,target:f.peId})
      tempSrc = f.peId
    })
  })
})
*/


$.ajax({
  url:"http://127.0.0.1:8000/api/teif_state",
  type:'get',
  dataType: 'json',
  success:function(res){
    var teData = JSON.parse(JSON.stringify(res))
    teData.forEach(e => {
      teAllData.push(e)
    })
  }
});

$.ajax({
  url:"http://127.0.0.1:8000/api/tenant_te_traffic",
  type:'get',
  dataType: 'json',
  success:function(res){
    var tenantData = JSON.parse(JSON.stringify(res))
    tenantData.result.forEach(e => {
      tenantAllData.push(e)
    })
  }
});

$.ajax({
  url:"http://127.0.0.1:8000/api/te_1",
  type:'get',
  dataType: 'json',
  success:function(res){
    var tePathData = JSON.parse(JSON.stringify(res))
    tePathData.results.item.forEach(e => {
      tePathAllData.push(e)
      teVisData[e.name] = []
      teVisData[e.name].push({name:e.srcPe,symbolSize:40})
      teVisLinks[e.name] = []
      var tempSrc = e.srcPe
      e.teTunnelPaths[0].paths.forEach(f => {
        teVisData[e.name].push({name:f.peId,symbolSize:40})
        teVisLinks[e.name].push({source:tempSrc,target:f.peId})
        tempSrc = f.peId
      })
    })
  }
});

export default {
  name: 'HelloWorld',
  data () {
    return{
      tenantAllData,
      dialogVisible: false,
      tun:'',
    }
  },
  methods:{
     checkTun(index, row) {
        console.log(index, row);
        this.dialogVisible=true;
        this.tun = row.tun;
     },
     handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
     },
     open(){
        const  myCharts = this.$echarts.init(this.$refs.myCharts,'dark');
        let option = {
          title: {
            text: this.tun + ' Info',
            top: 'top',
            left: 'right'
          },
          tooltip: {},
          animationDuration: 1500,
          animationEasingUpdate: 'quinticInOut',
          series : [
              {
                  type: 'graph',
                  layout: 'force',
                  force: { // 力引导图基本配置
                      // initLayout: , // 力引导的初始化布局，默认使用xy轴的标点
                      repulsion: 500, // 节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                      gravity: 0.02, // 节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                      edgeLength: 200, // 边的两个节点之间的距离，这个距离也会受 repulsion影响 。值越大则长度越长
                      layoutAnimation: true // 因为力引导布局会在多次迭代后才会稳定，这个参数决定是否显示布局的迭代动画
                      // 在浏览器端节点数据较多（>100）的时候不建议关闭，布局过程会造成浏览器假死。
                  },
                  draggable: false,
                  roam: false,
                  focusNodeAdjacency: true,
                  data:teVisData[this.tun],
                  links:teVisLinks[this.tun],
                  itemStyle: {
                      borderColor: '#fff',
                      borderWidth: 1,
                      shadowBlur: 10,
                      shadowColor: 'rgba(0, 0, 0, 0.3)'
                  },
                  label: {
                      position: 'right',
                      formatter: '{b}'
                  },
                  lineStyle: {
                      color: 'source',
                      curveness: 0.3
                  },
                  emphasis: {
                      lineStyle: {
                          width: 10
                      }
                  }
              }
          ]
        };


        myCharts.setOption(option)

        window.onresize = function(){
            myCharts.resize();
        }
        myCharts.on('click', function (params) {
            console.log(params);
        });
     }
  },
  mounted(){

  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

#myCharts{
    width: 100%;
    height: 500px;
    margin: 0 auto;
  }
</style>
