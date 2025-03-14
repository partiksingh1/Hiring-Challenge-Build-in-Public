<template>
  <div class="flex flex-col items-center p-4 min-h-screen">
    <div class="w-full max-w-3xl space-y-6">
      <!-- Game Selection Card -->
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Select Game</h2>
        
        <!-- Loading State for Game List -->
        <div v-if="isLoadingGames" class="flex justify-center items-center">
          <span>Loading Games...</span>
          <div class="ml-2 text-blue-600" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </div>
        
        <div v-else class="grid gap-3">
          <div 
            v-for="(config) in gameConfigs" 
            :key="config.id"
            class="border rounded-lg p-4 cursor-pointer transition-all hover:bg-blue-50 hover:border-blue-300"
            :class="{'border-blue-500': selectedGame && selectedGame.difficulty === config.difficulty}"
            @click="selectGame(config)"
          >
            <div class="flex justify-between items-center">
              <div>
                <h2 class="font-bold text-gray-800">Game : {{ config.gameName }}</h2>
                <h3 class="font-bold text-gray-800">Difficulty : {{ config.difficulty }}</h3>
                <p class="font-medium text-gray-600">Levels : {{ config.rounds }}</p>
              </div>
              <div class="text-blue-500" v-if="selectedGame && selectedGame.difficulty === config.difficulty">
                ✓
              </div>
            </div>
          </div>
        </div>
        
        <button
          class="mt-4 w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          :disabled="!selectedGame"
          @click="startGame"
        >
          Start Game
        </button>
      </div>

      <!-- Progress History Card -->
      <div v-if="userProgress.length" class="bg-white shadow rounded-lg p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4">Your Scores</h2>
        
        <!-- Loading State for Scores -->
        <div v-if="isLoadingProgress" class="flex justify-center items-center">
          <span>Loading Scores...</span>
          <div class="ml-2 text-blue-600">
            <span class="sr-only">Loading...</span>
          </div>
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="(progress, index) in userProgress" 
            :key="index" 
            class="flex justify-between items-center p-3 border-b last:border-b-0"
          >
            <div>
              <span class="font-medium">{{ progress.game_name }}</span>
            </div>
            <div class="font-bold text-lg">
              {{ progress.score }}
              <span class="text-xs text-gray-500">pts</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";
import router from "../../router";

interface GameConfig {
  id: string;
  difficulty: string;
  rounds: number;
  gameName: string;
}

interface UserProgress {
  game_name: string;
  score: number;
  is_completed: boolean;
}

interface User {
  uid: string;
}

export default {
  name: "UserDashboard",
  setup() {
    const gameConfigs = ref<GameConfig[]>([]);
    const selectedGame = ref<GameConfig | null>(null);
    const gameStarted = ref(false);
    const score = ref(0);
    const userProgress = ref<UserProgress[]>([]);

    // Loading states
    const isLoadingGames = ref(true);
    const isLoadingProgress = ref(true);

    // Fetch the game configurations
    const fetchGameConfigs = async () => {
      try {
        const response = await fetch("https://hiring-challenge-build-in-public-d76h.onrender.com/game/configure");
        const data = await response.json();
        gameConfigs.value = data;
      } catch (error) {
        console.error(error);
        alert("Error fetching game configurations.");
      } finally {
        isLoadingGames.value = false;
      }
    };

    // Fetch user progress
    const fetchUserProgress = async () => {
      const userString = localStorage.getItem("user");
      
      // Parse the user string into an object
      if (userString) {
        const user = JSON.parse(userString) as User;

        try {
          const response = await fetch(`https://hiring-challenge-build-in-public-d76h.onrender.com/game/scores/${user.uid}`);
          const data = await response.json();
          userProgress.value = data;
        } catch (error) {
          console.error(error);
          alert("Error fetching user progress.");
        } finally {
          isLoadingProgress.value = false;
        }
      } else {
        console.error("No user data found in local storage.");
        alert("No user data found. Please log in.");
      }
    };

    // Handle game selection
    const selectGame = (config: GameConfig) => {
      selectedGame.value = config;
    };

    // Start the game
    const startGame = () => {
      if (!selectedGame.value) return;
      gameStarted.value = true;
      router.push({
        name: 'game',
        query: {
          gameId: selectedGame.value.id,
        }
      });
    };

    // On component mounted, fetch the game configurations and user progress
    onMounted(() => {
      fetchGameConfigs();
      fetchUserProgress();
    });

    return {
      gameConfigs,
      selectedGame,
      gameStarted,
      score,
      userProgress,
      selectGame,
      startGame,
      isLoadingGames,
      isLoadingProgress,
    };
  },
};
</script>

