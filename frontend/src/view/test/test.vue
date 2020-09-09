<template>
    <div>
        <button @click="getUrl">请求</button>
    </div>
</template>

<script>
import $ from 'jquery'
export default {
    name: 'test',
    methods: {
        getUrl(){
            let url = '/api/monitor/vpn/history',
                params={
                    namespace: 'traffic',
                    metricNames: 'in_traffic,out_traffic',
                    startTime: '2020-08-19 14:47:20',
                    endTime: '2020-08-20 14:47:20'
                }
            $.get(url, params, (res)=>{
                if(res.code == 0){
                    alert(res.message)
                    console.log(res.data)
                }
            })
        }
    }
}
</script>

<style scoped>

</style>