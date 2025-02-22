import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import SubmitAssignment from "@/views/SubmitView.vue";
import Ranking from "@/views/RankingView.vue";

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/home', component: HomeView },
  { path: '/submit', component: SubmitAssignment },
  { path: '/ranking', component: Ranking }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router;
