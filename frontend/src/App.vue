<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'HelloWorld',
  data() {
    return {
    }
  },
  methods: {
    toView1(){
      if(location.pathname==='/demo/view1/'){
        location.reload();
      }
      else{
        this.$router.push({ path: '/demo/view1/' })
      }
    },
    toView2(){
      if(location.pathname==='/demo/view2/'){
        location.reload();
      }
      else{
        this.$router.push({ path: '/demo/view2/' })
      }
    },
    toView3(){
      if(location.pathname==='/demo/view3/'){
        location.reload();
      }
      else{
        this.$router.push({ path: '/demo/view3/' })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
