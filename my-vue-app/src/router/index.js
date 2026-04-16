import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 路由懒加载（添加 chunk 命名，便于打包后识别）
const Login = () => import(/* webpackChunkName: "login" */ '../views/Login.vue')           // 登录页面
const ImageRepair = () => import(/* webpackChunkName: "image-repair" */ '../views/ImageRepair.vue')  // 图像修复页面
const Dashboard = () => import(/* webpackChunkName: "dashboard" */ '../views/Dashboard.vue')      // 数据看板页面
const Profile = () => import(/* webpackChunkName: "profile" */ '../views/Profile.vue')          // 个人中心页面
const AppValue = () => import(/* webpackChunkName: "app-value" */ '../views/AppValue.vue')        // 应用价值页面
const TechRoadmap = () => import(/* webpackChunkName: "tech-roadmap" */ '../views/TechRoadmap.vue')  // 技术路线页面

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      requiresGuest: true,
      title: '登录 - 系统名称'  // 添加页面标题
    }
  },
  {
    path: '/',
    redirect: '/dashboard'  // 根路径重定向到dashboard
  },
  {
    path: '/image-repair',
    name: 'ImageRepair',
    component: ImageRepair,
    meta: {
      requiresAuth: true,
      title: '图像修复 - 系统名称'
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true,
      title: '数据看板 - 系统名称'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requiresAuth: true,
      title: '个人中心 - 系统名称'
    }
  },
  {
    path: '/app-value',
    name: 'AppValue',
    component: AppValue,
    meta: {
      requiresAuth: true,
      title: '应用价值 - 系统名称'
    }
  },
  {
    path: '/tech-roadmap',
    name: 'TechRoadmap',
    component: TechRoadmap,
    meta: {
      requiresAuth: true,
      title: '技术路线 - 系统名称'
    }
  },
  // 404页面处理
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),  // 使用HTML5 history模式（无#号）
  routes,                       // 传入路由配置
  // 滚动行为：切换路由时滚动到顶部
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 动态设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }

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
