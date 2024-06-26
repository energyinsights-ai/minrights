import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../clients/supabase'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import UnauthorizedView from '../views/UnauthorizedView.vue'
import Evaluation from '../views/Eval.vue'

let localUser;

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path:'/login',
      name: 'login',
      component: Login
    },
    {
      path:'/evaluation',
      name: 'evaluation',
      component:Evaluation
    },
    {
      path:'/register',
      name:'register',
      component:Register
    },
    {
      path:'/unauthorized',
      name:'unauthorized',
      component: UnauthorizedView
    },
    {
      path:'/myasset',
      name:'myasset',
      component: () => import('../views/MyAsset.vue'),
      meta: { requiresAuth: true },


    },
  ]
})

async function getUser(next) {
	localUser = await supabase.auth.getSession();
	if (localUser.data.session == null) {

		next('/login')
	}
	else {
		next();
	}
}


router.beforeEach((to, from, next) => {
	if (to.meta.requiresAuth) {
		getUser(next);
	}
	else {
		next();
	}
})


export default router
