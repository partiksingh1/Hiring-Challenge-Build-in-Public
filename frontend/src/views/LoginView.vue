<template>
  <div class="flex flex-col justify-center items-center py-6 px-4 sm:px-6 lg:px-8">
    <div class="w-full md:w-1/3">
      <img src="/logo.png" alt="Balance Scale Game" class="rounded-lg bg-yellow-300" />
    </div>
    <div class="max-w-md w-full space-y-8">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Login</h2>

      <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        {{ errorMessage }}
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="Email address"
            class="block w-full px-3 py-2 border border-gray-300 text-gray-900 rounded-t-md sm:text-sm"
          />
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="Password"
            class="block w-full px-3 py-2 border border-gray-300 text-gray-900 rounded-b-md sm:text-sm"
          />
        </div>

        <button type="submit" :disabled="loading" class="w-full py-2 bg-black text-white rounded-md">
          <span v-if="loading" class="animate-spin mr-2">⏳</span> Login
        </button>
      </form>

      <button @click="handleGoogleLogin" class="w-full py-2 mt-4 bg-gray-200 text-black rounded-md">
        Sign in with Google
      </button>

      <p class="mt-4 text-center text-sm">
        Don't have an account?
        <router-link to="/register" class="text-indigo-600">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { auth, db } from "../firebase";
import { signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from "firebase/auth";
import { getDoc, doc } from "firebase/firestore";
import { useAuthStore } from "../stores/userStore";

const router = useRouter();
const store = useAuthStore();

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);

const provider = new GoogleAuthProvider();

async function getUserRole(userId) {
  try {
    const userDoc = await getDoc(doc(db, "users", userId));
    return userDoc.exists() ? userDoc.data().role : null;
  } catch (error) {
    console.error("Error fetching user role:", error);
    return null;
  }
}

const handleLogin = async () => {
  loading.value = true;
  console.log("Logging in...");
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value);
    const fetchedRole = await getUserRole(userCredential.user.uid);
    console.log("Fetched Role:", fetchedRole);
    
    if (fetchedRole) {
      store.setUser (userCredential.user, fetchedRole);
      router.push(fetchedRole === "admin" ? "/admin-dashboard" : "/dashboard");
    } else {
      errorMessage.value = "User  role not found.";
    }
  } catch (error) {
    console.error("Email Login Error:", error);
    errorMessage.value = "Incorrect email or password.";
  } finally {
    loading.value = false;
    console.log("Loading finished.");
  }
};

const handleGoogleLogin = async () => {
  loading.value = true;
  try {
    const result = await signInWithPopup(auth, provider);
    const role = await getUserRole(result.user.uid);

    store.setUser(result.user, role);
    router.push(role === "admin" ? "/admin-dashboard" : "/dashboard");
  } catch (error) {
    console.error("Google Login Error:", error);
    errorMessage.value = "Google sign-in failed.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  onAuthStateChanged(auth, async (user) => {
    if (user) {
      const role = await getUserRole(user.uid);
      store.setUser(user, role);
      router.push(role === "admin" ? "/admin-dashboard" : "/dashboard");
    }
  });
});
</script>
