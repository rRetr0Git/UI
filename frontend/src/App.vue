<template>
  <div>
    <el-menu
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b">
      <el-menu-item index="1" @click="toView1">View 1</el-menu-item>
      <el-submenu index="2">
        <template slot="title">View 2</template>
        <el-menu-item index="2-1">Sub 1</el-menu-item>
        <el-menu-item index="2-2">Sub 2</el-menu-item>
        <el-menu-item index="2-3">Sub 3</el-menu-item>
      </el-submenu>
      <el-menu-item index="3" @click="toView3">View 3</el-menu-item>
      <el-menu-item index="4"><a href="https://www.ele.me" target="_blank">View 4</a></el-menu-item>
    </el-menu>
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
      this.$router.push({ path: '/view1' })
    },
    toView3(){
      this.$router.push({ path: '/view3' })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
