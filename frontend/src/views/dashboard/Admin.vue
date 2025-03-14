<template>
  <div class="flex flex-col items-center space-y-4 p-6">
    <div class="bg-white shadow-xl rounded-lg p-6 w-full max-w-4xl">
      <h2 class="text-2xl font-semibold mb-4">Game Settings</h2>
      <form @submit.prevent="configureGame" class="space-y-4">
        <div>
          <label for="difficulty" class="block text-lg">Difficulty</label>
          <select id="difficulty" v-model="gameConfig.difficulty" class="w-full border border-gray-300 p-2 rounded">
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <div>
          <label for="name" class="block text-lg">Game Name</label>
          <input
            id="name"
            type="text"
            v-model="gameConfig.gameName"
            class="w-full border border-gray-300 p-2 rounded"
            required
          />
        </div>
        <div>
          <label for="rounds" class="block text-lg">Rounds</label>
          <input
            id="rounds"
            type="number"
            v-model="gameConfig.rounds"
            class="w-full border border-gray-300 p-2 rounded"
            required
          />
        </div>
        <button
          type="submit"
          class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 focus:outline-none"
        >
          Save Game Configuration
        </button>
      </form>
      <div class="bg-white shadow-xl rounded-lg p-6 w-full max-w-4xl">
      <table class="min-w-full table-auto">
        <thead>
          <tr class="bg-gray-100">
            <th class="px-4 py-2 text-left">Game Name</th>
            <th class="px-4 py-2 text-left">Difficulty</th>
            <th class="px-4 py-2 text-left">Rounds</th>
            <th class="px-4 py-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(config, index) in allGameConfigs" :key="index" class="border-b">
            <td class="px-4 py-2">{{ config.gameName }}</td>
            <td class="px-4 py-2">{{ config.difficulty }}</td>
            <td class="px-4 py-2">{{ config.rounds }}</td>
            <td class="px-4 py-2">
              <button @click="deleteGameConfig(config.id)" class="text-red-500 hover:text-red-700">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>

    <div class="bg-white shadow-xl rounded-lg p-6 w-full max-w-4xl">
      <h2 class="text-2xl font-semibold mb-4">User  Progress</h2>
      <table class="min-w-full table-auto">
        <thead>
          <tr class="bg-gray-100">
            <th class="px-4 py-2 text-left">User </th>
            <th class="px-4 py-2 text-left">Game Name</th>
            <th class="px-4 py-2 text-left">Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(progress, index) in allUserProgress" :key="index" class="border-b">
            <td class="px-4 py-2">{{ progress.email }}</td>
            <td class="px-4 py-2">{{ progress.game_name }}</td>
            <td class="px-4 py-2">{{ progress.score }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from "vue";

interface GameConfig {
  id?: string; // Add id to the GameConfig interface
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
    const allGameConfigs = ref<GameConfig[]>([]); // Store all game configurations

    // Function to configure the game settings
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
          fetchGameConfigs(); // Refresh the game configurations
        } else {
          alert("Failed to save game configuration.");
        }
      } catch (error) {
        console.error(error);
        alert("Error configuring the game.");
      }
    };

    // Fetch all user progress
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

    // Fetch all game configurations
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

    // Delete a game configuration
    const deleteGameConfig = async (gameId: string | undefined) => {
      try {
        const response = await fetch(`https://hiring-challenge-build-in-public-d76h.onrender.com/game/configure/${gameId}`, {
          method: "DELETE",
        });

        if (response.ok) {
          alert("Game configuration deleted successfully!");
          fetchGameConfigs(); // Refresh the game configurations
        } else {
          alert("Failed to delete game configuration.");
        }
      } catch (error) {
        console.error(error);
        alert("Error deleting game configuration.");
      }
    };

    // Fetch user progress and game configurations when the component is mounted
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

<style scoped>
/* You can add custom styles if needed */
</style>