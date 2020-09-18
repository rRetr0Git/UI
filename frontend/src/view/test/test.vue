<template>
    <div>
        <button @click="getUrl">请求(无鉴权)</button>
        <button @click="getAuthorizationUrl">请求(有鉴权)</button>
        <div v-html="data"></div>
    </div>
</template>

<script>
import $ from 'jquery'
export default {
    name: 'test',
    data(){
        return {
            data: null
        }
    },
    methods: {
        getUrl(){
            this.data = '请求中'
            let url = '/api/monitor/vpn/history',
                params={
                    namespace: 'traffic',
                    metricNames: 'in_traffic,out_traffic',
                    startTime: '2020-08-19 14:47:20',
                    endTime: '2020-08-20 14:47:20'
                }
            $.get(url, params, (res)=>{
                if(res.code == 0){
                    this.data = res
                }
            })
        },
        getAuthorizationUrl(){
            this.data = '请求中'
            let url = '/api/api/sr/config/terra-te-svc:te-path/all',
                headers = {
                    'Authorization': 'Bearer 9373b74f-ad19-4ba0-8d61-19a6deece69a'
                };
            $.ajax({
                type: 'get',
                url,
                headers,
                success: (res) => {
                    // 请求成功
                    this.data = res
                },
                error: (err) => {
                    // 请求失败
                    this.data = err
                }
            })

        }
    }
}
</script>

<style scoped>

</style>