
  // firebase.ts
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";


const firebaseConfig = {
    apiKey: "AIzaSyBYj5gPF9SnAbVUzPJUTCSwTrmkCfPkSbY",
    authDomain: "balance-it-a7104.firebaseapp.com",
    projectId: "balance-it-a7104",
    storageBucket: "balance-it-a7104.firebasestorage.app",
    messagingSenderId: "630956322456",
    appId: "1:630956322456:web:90c1deb0b3b67ecff32aed",
    measurementId: "G-H1VDWZF0DG"
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
