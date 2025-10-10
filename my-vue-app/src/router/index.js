//创建路由配置
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 路由懒加载
const Login = () => import('../views/Login.vue')           // 登录页面
const ImageRepair = () => import('../views/ImageRepair.vue')  // 图像修复页面
const Dashboard = () => import('../views/Dashboard.vue')      // 数据看板页面
const Profile = () => import('../views/Profile.vue')          // 个人中心页面
const AppValue = () => import('../views/AppValue.vue')        // 应用价值页面
const TechRoadmap = () => import('../views/TechRoadmap.vue')  // 技术路线页面

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }  // 仅未登录时可访问
  },
  {
    path: '/',
    redirect: '/dashboard'  // 根路径重定向到dashboard
  },
  {
    path: '/image-repair',
    name: 'ImageRepair',
    component: ImageRepair,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/dashboard',
    name: 'Dashboard', 
    component: Dashboard,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/app-value',
    name: 'AppValue',
    component: AppValue,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/tech-roadmap',
    name: 'TechRoadmap',
    component: TechRoadmap,
    meta: { requiresAuth: true }  // 需要登录
  },
  // 404页面处理
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),  // 使用HTML5 history模式（无#号）
  routes                        // 传入路由配置
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 检查路由是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 如果需要认证但未登录，跳转到登录页
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    // 如果已登录但访问登录页，跳转到首页
    next('/dashboard')
  } else {
    // 正常放行
    next()
  }
})

export default router