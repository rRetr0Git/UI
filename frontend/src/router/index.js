import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import View1 from '@/components/View1'
import App from '../App'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/view3',
      component: HelloWorld
    },
    {
      path: '/view1',
      component: View1
    }
  ],
  mode: 'history'
})
