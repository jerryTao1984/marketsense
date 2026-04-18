import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CategoryView from '../views/CategoryView.vue'
import QuizView from '../views/QuizView.vue'
import LoginView from '../views/LoginView.vue'
import ProfileView from '../views/ProfileView.vue'
import WrongAnswersView from '../views/WrongAnswersView.vue'
import ReviewQuizView from '../views/ReviewQuizView.vue'
import HistoryView from '../views/HistoryView.vue'
import { useUserStore } from '../stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', component: LoginView },
    { path: '/', component: HomeView },
    { path: '/category/:categoryId', component: CategoryView },
    { path: '/quiz/:categoryId/:levelId', component: QuizView },
    { path: '/profile', component: ProfileView },
    { path: '/wrong-answers', component: WrongAnswersView },
    { path: '/review/:levelId', component: ReviewQuizView },
    { path: '/history', component: HistoryView },
  ],
})

router.beforeEach((to) => {
  if (to.path === '/login') return
  const userStore = useUserStore()
  // 如果还没恢复过登录态，先从 localStorage 恢复
  if (!userStore.isLoggedIn) {
    userStore.restoreLogin()
  }
  // 恢复后仍然未登录，跳转登录页
  if (!userStore.isLoggedIn) {
    return '/login'
  }
})

export default router
