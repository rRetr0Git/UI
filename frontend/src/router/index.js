import Vue from 'vue'
import Router from 'vue-router'
import View3 from '@/components/View3'
import View2 from '@/components/View2'
import View1 from '@/components/View1'
import View4 from '@/components/View4'
import View5 from '@/components/View5'
import App from '../App'
Vue.use(Router)
export default new Router({
  routes: [
    {
      path: '/demo/view1/',
      component: View1
    },
    {
      path: '/demo/view3/',
      component: View3
    },
    {
      path: '/demo/view2/',
      component: View2
    },
    {
      path: '/demo/view4/',
      component: View4
    },
    {
      path: '/demo/view5/',
      component: View5
    },
    {
      path: '/test',
      component: ()=> import ('@/view/test')
    }
  ],
  mode: 'history'
})
