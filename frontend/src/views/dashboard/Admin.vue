<template>
  <div class="flex flex-col items-center space-y-4 p-4 sm:p-6 min-h-screen bg-gray-100">
    <!-- Game Settings Section -->
    <div class="bg-white shadow-xl rounded-lg p-4 sm:p-6 w-full max-w-4xl">
      <h2 class="text-xl sm:text-2xl font-semibold mb-4">Game Settings</h2>
      <form @submit.prevent="configureGame" class="space-y-4">
        <div>
          <label for="difficulty" class="block text-base sm:text-lg">Difficulty</label>
          <select
            id="difficulty"
            v-model="gameConfig.difficulty"
            class="w-full border border-gray-300 p-2 rounded text-sm sm:text-base"
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <div>
          <label for="name" class="block text-base sm:text-lg">Game Name</label>
          <input
            id="name"
            type="text"
            v-model="gameConfig.gameName"
            class="w-full border border-gray-300 p-2 rounded text-sm sm:text-base"
            required
          />
        </div>
        <div>
          <label for="rounds" class="block text-base sm:text-lg">Rounds</label>
          <input
            id="rounds"
            type="number"
            v-model="gameConfig.rounds"
            class="w-full border border-gray-300 p-2 rounded text-sm sm:text-base"
            required
          />
        </div>
        <button
          type="submit"
          class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none w-full sm:w-auto"
        >
          Save Game Configuration
        </button>
      </form>

      <!-- Game Configurations Table -->
      <div class="mt-6 overflow-x-auto">
        <table class="min-w-full table-auto text-sm sm:text-base">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-2 sm:px-4 py-2 text-left">Game Name</th>
              <th class="px-2 sm:px-4 py-2 text-left">Difficulty</th>
              <th class="px-2 sm:px-4 py-2 text-left">Rounds</th>
              <th class="px-2 sm:px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(config, index) in allGameConfigs" :key="index" class="border-b">
              <td class="px-2 sm:px-4 py-2">{{ config.gameName }}</td>
              <td class="px-2 sm:px-4 py-2">{{ config.difficulty }}</td>
              <td class="px-2 sm:px-4 py-2">{{ config.rounds }}</td>
              <td class="px-2 sm:px-4 py-2">
                <button
                  @click="deleteGameConfig(config.id)"
                  class="text-red-500 hover:text-red-700 text-sm sm:text-base"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- User Progress Section -->
    <div class="bg-white shadow-xl rounded-lg p-4 sm:p-6 w-full max-w-4xl">
      <h2 class="text-xl sm:text-2xl font-semibold mb-4">User Progress</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full table-auto text-sm sm:text-base">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-2 sm:px-4 py-2 text-left">User</th>
              <th class="px-2 sm:px-4 py-2 text-left">Game Name</th>
              <th class="px-2 sm:px-4 py-2 text-left">Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(progress, index) in allUserProgress" :key="index" class="border-b">
              <td class="px-2 sm:px-4 py-2">{{ progress.email }}</td>
              <td class="px-2 sm:px-4 py-2">{{ progress.game_name }}</td>
              <td class="px-2 sm:px-4 py-2">{{ progress.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";

interface GameConfig {
  id?: string;
  gameName: string;
  difficulty: string;
  rounds: number;
}

interface UserProgress {
  email: string;
  game_name: string;
  score: number;
  is_completed: boolean;
}

export default {
  name: "AdminDashboard",
  setup() {
    const gameConfig = ref<GameConfig>({
      gameName: "",
      difficulty: "easy",
      rounds: 10,
    });
    const allUserProgress = ref<UserProgress[]>([]);
    const allGameConfigs = ref<GameConfig[]>([]);

    const configureGame = async () => {
      try {
        const response = await fetch("https://hiring-challenge-build-in-public-d76h.onrender.com/game/configure", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(gameConfig.value),
        });

        if (response.ok) {
          alert("Game configuration saved successfully!");
          fetchGameConfigs();
        } else {
          alert("Failed to save game configuration.");
        }
      } catch (error) {
        console.error(error);
        alert("Error configuring the game.");
      }
    };

    const fetchUserProgress = async () => {
      try {
        const response = await fetch("https://hiring-challenge-build-in-public-d76h.onrender.com/game/users/progress");
        const data = await response.json();
        allUserProgress.value = data;
      } catch (error) {
        console.error(error);
        alert("Error fetching user progress.");
      }
    };

    const fetchGameConfigs = async () => {
      try {
        const response = await fetch("https://hiring-challenge-build-in-public-d76h.onrender.com/game/configure");
        const data = await response.json();
        allGameConfigs.value = data;
      } catch (error) {
        console.error(error);
        alert("Error fetching game configurations.");
      }
    };

    const deleteGameConfig = async (gameId: string | undefined) => {
      try {
        const response = await fetch(`https://hiring-challenge-build-in-public-d76h.onrender.com/game/configure/${gameId}`, {
          method: "DELETE",
        });

        if (response.ok) {
          alert("Game configuration deleted successfully!");
          fetchGameConfigs();
        } else {
          alert("Failed to delete game configuration.");
        }
      } catch (error) {
        console.error(error);
        alert("Error deleting game configuration.");
      }
    };

    onMounted(() => {
      fetchUserProgress();
      fetchGameConfigs();
    });

    return {
      gameConfig,
      allUserProgress,
      allGameConfigs,
      configureGame,
      deleteGameConfig,
    };
  },
};
</script>