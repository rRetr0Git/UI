import Vue from 'vue'
import Router from 'vue-router'
import View3 from '@/components/View3'
import View1 from '@/components/View1'
import App from '../App'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/view3',
      component: View3
    },
    {
      path: '/view1',
      component: View1
    }
  ],
  mode: 'history'
})
