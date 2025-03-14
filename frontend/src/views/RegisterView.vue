<template>
  <div class="flex flex-col justify-center items-center py-6 px-4 sm:px-6 lg:px-8">
    <div class="w-full md:w-1/3">
      <img src="/logo.png" alt="Balance Scale Game" class="rounded-lg bg-yellow-300" />
    </div>
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Create a new account</h2>
      </div>
      
      <!-- Registration Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm -space-y-px">
          
          <!-- Email Input -->
          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input
              id="email-address"
              type="email"
              required
              v-model="email"
              class="input-field"
              placeholder="Email address"
            />
          </div>
          
          <!-- Password Input -->
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              type="password"
              required
              v-model="password"
              class="input-field"
              placeholder="Password"
            />
          </div>
          
          <!-- Role Selection -->
          <div>
            <label for="role" class="sr-only">Role</label>
            <select id="role" v-model="role" required class="input-field">
              <option value="" disabled>Select your role</option>
              <option value="user">USER</option>
              <option value="admin">ADMIN</option>
            </select>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>

        <!-- Register Button -->
        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-black hover:bg-white hover:text-black focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <span v-if="loading">Loading...</span>
            <span v-else>Register</span>
          </button>
        </div>

        <!-- Link to Login Page -->
        <button @click="handleGoogleSignUp" class="w-full py-2 mt-4 bg-gray-200 text-black rounded-md">
        Sign up with Google
      </button>
        <div class="flex items-center justify-center">
          <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
            Already have an account? Sign in
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { doc, setDoc } from "firebase/firestore";
import { auth, db } from "../firebase";

const email = ref("");
const password = ref("");
const role = ref("");
const error = ref("");
const loading = ref(false);
const router = useRouter();

const handleRegister = async () => {
  if (!role.value) {
    error.value = "Please select a role";
    return;
  }

  try {
    loading.value = true;
    error.value = "";
    
    // Register user with Firebase Auth
    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value);
    const user = userCredential.user;
    
    // Store user role in Firestore
    await setDoc(doc(db, "users", user.uid), {
      email: email.value,
      role: role.value,
    });
    
    // Redirect based on role
    if (role.value === "admin") {
      router.push("/admin-dashboard");
    } else {
      router.push("/dashboard");
    }
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
// Handle Google Sign-Up
const handleGoogleSignUp = async () => {
  try {
    loading.value = true;
    error.value = "";

    // Set up Google provider
    const provider = new GoogleAuthProvider();

    // Sign in with Google popup
    const result = await signInWithPopup(auth, provider);
    const user = result.user;

    // Store user with "user" role in Firestore (force "user" role even if they choose admin)
    await setDoc(doc(db, "users", user.uid), {
      email: user.email,
      role: "user", // Only assign "user" role
    });

    // Redirect to the dashboard
    router.push("/dashboard");
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>



<style scoped>
.input-field {
  @apply appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm;
}
</style>