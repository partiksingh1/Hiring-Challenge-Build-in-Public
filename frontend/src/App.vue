<template>
  <div class="min-h-screen bg-gradient-to-b from-sky-100 to-indigo-50">
    <nav class="bg-yellow-300 text-white p-4">
      <div class="container mx-auto flex justify-between items-center text-black">
        <router-link to="/" class="text-xl font-bold text-black">Comini Learning</router-link>
        <div class="flex space-x-4">
          <template v-if="authStore.user">
            <router-link v-if="authStore.role === 'user'" to="/dashboard" class="hover:text-indigo-200">Dashboard</router-link>
            <button @click="handleLogout" class="hover:text-indigo-200">Logout</button>
            <router-link v-if="authStore.role === 'admin'" to="/admin-dashboard" class="hover:text-indigo-200">Dashboard</router-link>
          </template>
          <template v-else>
            <router-link to="/login" class="hover:text-indigo-200">Login</router-link>
            <router-link to="/register" class="hover:text-indigo-200">Register</router-link>
          </template>
        </div>
      </div>
    </nav>
    <main class="container mx-auto p-4">
      <div v-if="isLoading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
      <router-view v-else />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "./stores/userStore";

const authStore = useAuthStore();
const router = useRouter();
const isLoading = ref(true);  // Added loading state

onMounted(async () => {
  try {
    await authStore.checkSession();
  } catch (error) {
    console.error("Session check failed:", error);
  } finally {
    isLoading.value = false;  // Ensure loading stops even on error
  }
});

const handleLogout = async () => {
  try {
    await authStore.logout();
    router.push("/login");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};
</script>