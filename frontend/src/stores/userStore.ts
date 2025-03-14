import { defineStore } from "pinia";
import { 
  signInWithEmailAndPassword, 
  signOut, 
  createUserWithEmailAndPassword, 
  onAuthStateChanged, 
  type User 
} from "firebase/auth";
import { auth, db } from "../firebase";
import { doc, getDoc } from "firebase/firestore";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    role: null as string | null,
  }),

  actions: {
    async register(email: string, password: string, role: string) {  // Changed 'any' to 'string'
      try {
        const userCred = await createUserWithEmailAndPassword(auth, email, password);
        await fetch("http://localhost:8000/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, role }),  // Removed password from body for security
        });
        const userRole = await this.getUserRole(userCred.user.uid);
        this.setUser(userCred.user, userRole);
      } catch (error) {
        console.error("Registration error:", error);
        throw error;  // Allow caller to handle the error
      }
    },

    async login(email: string, password: string) {
      try {
        const userCred = await signInWithEmailAndPassword(auth, email, password);
        const userRole = await this.getUserRole(userCred.user.uid);
        this.setUser(userCred.user, userRole);
      } catch (error) {
        console.error("Login error:", error);
        throw error;
      }
    },

    async getUserRole(userId: string): Promise<string | null> {  // Added return type
      try {
        const userDoc = await getDoc(doc(db, "users", userId));
        return userDoc.exists() ? userDoc.data().role : null;
      } catch (error) {
        console.error("Error fetching role:", error);
        return null;
      }
    },

    setUser(user: User | null, role: string | null) {
      this.user = user;
      this.role = role;
      localStorage.setItem("user", user ? JSON.stringify(user) : "null");
      localStorage.setItem("role", role ?? "null");
    },

    async checkSession() {
      return new Promise<void>((resolve) => {  // Added Promise for better async handling
        onAuthStateChanged(auth, async (user) => {
          if (user) {
            const role = await this.getUserRole(user.uid);
            this.setUser(user, role);
          } else {
            this.setUser(null, null);
          }
          resolve();
        });
      });
    },

    async logout() {
      try {
        await signOut(auth);
        this.setUser(null, null);
        localStorage.removeItem("user");
        localStorage.removeItem("role");
      } catch (error) {
        console.error("Logout error:", error);
        throw error;
      }
    },
  },
});