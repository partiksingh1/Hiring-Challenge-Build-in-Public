
  // firebase.ts
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";


const firebaseConfig = {
  apiKey: "AIzaSyAD8XhF7foCf3tSRiZRLi3zvWT1MaLrJZc",
  authDomain: "balancescale-4074d.firebaseapp.com",
  projectId: "balancescale-4074d",
  storageBucket: "balancescale-4074d.firebasestorage.app",
  messagingSenderId: "787730771629",
  appId: "1:787730771629:web:109e29b2df474c3de7a024",
  measurementId: "G-JZ8TW4FE77"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };
