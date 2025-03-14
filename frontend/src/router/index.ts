import { createRouter, createWebHistory } from "vue-router";
import GameView from "../views/GameView.vue";
import LoginView from "../views/LoginView.vue";
import Admin from "../views/dashboard/Admin.vue";
import Student from "../views/dashboard/Student.vue";
import RegisterView from "../views/RegisterView.vue";
import HomeView from "../views/HomeView.vue";

const routes = [
  { path: "/",component: HomeView },
  { path: "/login", component: LoginView },
  { path: "/register", component: RegisterView },
  { path: "/admin-dashboard", component: Admin },
  { path: "/game",name:"game",  component: GameView },
  { path: "/dashboard", component: Student}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// // Fix: Call `useAuthStore()` inside the `beforeEach` hook, not globally
// router.beforeEach(async (to, _from, next) => {
//   const authStore = useAuthStore(); // This must be called inside a function
//   await authStore.checkSession();

//   if (to.meta.requiresAuth) {
//     if (authStore.role === to.meta.role) next();
//     else next("/login");
//   } else {
//     next();
//   }
// });

export default router;
