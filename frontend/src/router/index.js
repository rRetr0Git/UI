import Vue from 'vue'
import Router from 'vue-router'
import View3 from '@/components/View3'
import View2 from '@/components/View2'
import View1 from '@/components/View1'
import App from '../App'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/demo/view3/',
      component: View3
    },
    {
      path: '/demo/view2/',
      component: View2
    },
    {
      path: '/demo/view1/',
      component: View1
    }
  ],
  mode: 'history'
})
