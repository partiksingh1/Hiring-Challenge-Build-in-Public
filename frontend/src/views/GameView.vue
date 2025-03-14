<template>
  <div class="flex flex-col items-center justify-center min-h-screen p-4">
    <h1 class="text-3xl font-bold text-blue-800 mb-2">Balance Scale Addition Game</h1>
    <p class="text-lg text-gray-700 mb-6">Find numbers that add up to match the target value!</p>

    <!-- Start Screen -->
    <div v-if="!gameStarted" class="w-full max-w-3xl bg-white rounded-xl shadow-lg p-6 mb-6 text-center">
      <h2 class="text-2xl font-semibold text-blue-800 mb-4">Ready to Play?</h2>
      <button 
        @click="startGame"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg font-bold shadow-md hover:bg-blue-700 transition-colors m-2"
      >
        Start Game
      </button>
      <button 
        @click="goToDashboard"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg font-bold shadow-md hover:bg-blue-700 transition-colors m-2"
      >
        Dashboard
      </button>
    </div>

    <!-- Game container (shown only when game has started) -->
    <div v-if="gameStarted" class="w-full max-w-3xl bg-white rounded-xl shadow-lg p-6 mb-6">
      <!-- Level info -->
      <div class="flex justify-between items-center mb-4">
        <h1>{{ gameName }} - {{ difficulty }} ({{ totalRounds }} rounds)</h1>
        <div class="text-lg font-semibold text-gray-800">Level: {{ currentRound - 1 }}</div>
        <div class="text-lg font-semibold text-purple-700">Target: {{ targetNumber }}</div>
        <div class="text-lg font-semibold text-green-700">Score: {{ score }}</div>
        <div class="text-lg font-semibold text-red-700">Time: {{ timeLeft }}s</div>
      </div>

      <!-- Balance scale -->
<!-- Balance scale -->
<div class="relative mb-10 h-56">
  <!-- Fulcrum -->
  <div class="absolute left-1/2 bottom-0 w-8 h-28 bg-gradient-to-t from-gray-700 to-gray-600 -ml-4 shadow-lg"></div>
  <div class="absolute left-1/2 bottom-28 w-20 h-8 bg-gray-800 rounded-full -ml-10 shadow-md border-2 border-gray-600"></div>

  <!-- Scale beam -->
  <div 
    class="absolute left-1/2 bottom-32 w-3/4 h-4 bg-gradient-to-r from-amber-900 to-amber-700 rounded-full origin-center transform -translate-x-1/2 shadow-lg"
    :style="{ transform: `translate(-50%, 0) rotate(${-scaleRotation}deg)` }"
  ></div>

  <!-- Scale plates -->
  <div 
    class="absolute left-1/4 rounded-full w-28 h-4 flex items-center justify-center transform -translate-x-1/2"
    :style="{ bottom: `${90 - scaleRotation * 2}px` }"
  >
    <div 
      class="absolute -top-16 p-4 bg-purple-200 rounded-xl text-purple-800 font-bold text-xl shadow-sm border border-purple-300"
      :style="{ transform: `translateY(${scaleRotation * 2}px)` }"
    >
      {{ currentTotal }}
    </div>
  </div>

  <div 
    class="absolute left-3/4 rounded-full w-28 h-4 flex items-center justify-center transform -translate-x-1/2"
    :style="{ bottom: `${90 + scaleRotation * 2}px` }"
  >
    <div 
      class="absolute -top-16 p-4 bg-purple-200 rounded-xl text-purple-800 font-bold text-xl shadow-sm border border-purple-300"
      :style="{ transform: `translateY(${-scaleRotation * 2}px)` }"
    >
      {{ targetNumber }}
    </div>
  </div>
</div>


      <!-- Number selection -->
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div v-for="number in availableNumbers" :key="number" 
             class="flex items-center justify-center">
          <button 
            @click="addNumber(number)"
            class="w-16 h-16 rounded-lg bg-blue-500 text-white text-xl font-bold shadow-md hover:bg-blue-600 transition-colors"
            :disabled="selectedNumbers.length >= 3"
          >
            {{ number }}
          </button>
        </div>
      </div>

      <!-- Selected numbers display -->
      <div class="flex justify-center space-x-4 mb-6 h-16">
        <div v-for="(number, index) in selectedNumbers" :key="'selected-' + index" 
          class="w-14 h-14 rounded-lg bg-blue-700 text-white flex items-center justify-center text-xl font-bold relative group">
          {{ number }}
          <button 
            @click="removeNumber(index)"
            class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
          >
            ×
          </button>
        </div>

        <div v-for="empty in 3 - selectedNumbers.length" :key="'empty-' + empty" 
             class="w-14 h-14 rounded-lg border-2 border-dashed border-gray-300"></div>
      </div>

      <!-- Controls -->
      <div class="flex justify-center space-x-4">
        <button 
          @click="checkAnswer"
          class="px-6 py-3 bg-green-600 text-white rounded-lg font-bold shadow-md hover:bg-green-700 disabled:bg-gray-400 transition-colors"
          :disabled="selectedNumbers.length === 0 || timeLeft <= 0"
        >
          Check
        </button>
        <button 
          @click="resetSelection"
          class="px-6 py-3 bg-yellow-500 text-white rounded-lg font-bold shadow-md hover:bg-yellow-600 transition-colors"
          :disabled="timeLeft <= 0"
        >
          Reset
        </button>
      </div>
    </div>

    <!-- Feedback message -->
    <div 
      v-if="feedbackMessage && gameStarted" 
      class="w-full max-w-3xl p-4 rounded-lg text-center text-lg font-semibold mb-4"
      :class="feedbackType === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
    >
      {{ feedbackMessage }}
    </div>

    <!-- Rules -->
    <div class="w-full max-w-3xl bg-white rounded-xl shadow-lg p-4 text-gray-700">
      <h2 class="text-xl font-bold text-blue-800 mb-2">How to Play:</h2>
      <ul class="list-disc pl-5 space-y-1">
        <li>Select numbers from the buttons that add up to the target value</li>
        <li>You can use up to 3 numbers for each sum</li>
        <li>Watch the scale tilt to see if your sum is too large or too small</li>
        <li>Earn 1 point per correct answer + bonus points for time remaining (1 point per 5 seconds left)</li>
        <li>Each correct answer earns 1 point</li>
        <li>The game gets harder as you level up!</li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, nextTick, onMounted } from 'vue';
interface User{
  uid:string
}

export default defineComponent({
  name: 'BalanceScaleGame',
  data() {
    return {
      gameStarted: false,
      targetNumber: 0,
      availableNumbers: [] as number[],
      selectedNumbers: [] as number[],
      currentTotal: 0,
      scaleRotation: 0,
      score: 0,
      level: 1,
      feedbackMessage: '',
      feedbackType: '',
      totalRounds: 0,
      correctAnswers: 0,
      currentRound: 1,
      maxAddends: 3,
      isLoading: false,
      timeLeft: 30,
      timerInterval: null as number | null,
      maxTime: 30,
      gameName: '',
      difficulty: '',
      gameId: '',
    };
  },
  async mounted() {
    console.log('Component mounted, waiting for user to start game...');
    // Use this.$route to access route parameters
    const route = this.$route;
    console.log('Route parameters:', route.query);
    this.gameId = route.query.gameId as string;
    this.gameName = route.query.gameName as string;
    this.difficulty = route.query.difficulty as string;
    this.totalRounds = parseInt(route.query.rounds as string);
    console.log('Route parameters:', this.gameId, this.gameName, this.difficulty, this.totalRounds);
  },
  methods: {
    goToDashboard() {
      this.$router.push('/dashboard'); // Navigate to the /dashboard route
    },
    async startGame() {
      console.log('Starting game...');
      this.gameStarted = true;
      this.isLoading = true;
      await this.fetchGameConfig();
      this.isLoading = false;
    },
    async fetchGameConfig() {
      console.log('Fetching game configuration...');
      try {
        const response = await fetch(`http://localhost:8000/game/configure/${this.gameId}`);
        const config = await response.json();
        this.totalRounds = config.rounds;
        this.difficulty = config.difficulty;
        this.gameName = config.gameName;
        console.log('Game configuration fetched:', config);
        await this.startNewRound();
      } catch (error) {
        console.error('Error fetching game configuration:', error);
        await this.startNewRound();
      }
    },
    startTimer() {
      if (this.timerInterval) clearInterval(this.timerInterval);
      this.timeLeft = this.maxTime;
      this.timerInterval = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
          console.log('Time left:', this.timeLeft);
        } else {
          clearInterval(this.timerInterval!);
          this.feedbackMessage = 'Time’s up! Starting new round...';
          this.feedbackType = 'error';
          setTimeout(() => this.startNewRound(), 1000);
        }
      }, 1000);
    },
    async startNewRound() {
      console.log('Starting new round...');
      this.isLoading = true;
      if (this.timerInterval) clearInterval(this.timerInterval);

      this.selectedNumbers = [];
      this.currentTotal = 0;
      this.scaleRotation = 0;
      this.feedbackMessage = '';
      this.feedbackType = '';

      const maxTarget = Math.min(10 + this.level * 5, 50);
      this.targetNumber = Math.floor(Math.random() * (maxTarget - 5)) + 5;
      console.log('New target number:', this.targetNumber);

      await this.generateAvailableNumbers();

      if (this.currentRound > 1) {
        this.level = Math.floor((this.correctAnswers / 2) + 1);
        console.log('Level updated to:', this.level);
      }
      this.currentRound++;
      console.log('Current round:', this.currentRound);

      await nextTick();
      this.startTimer();
      this.isLoading = false;
      console.log('New round started, loading complete.');
    },
    async generateAvailableNumbers() {
      console.log('Generating available numbers...');
      const numbers = new Set();
      const maxNumber = Math.min(Math.floor(this.targetNumber * 0.8), 20);
      
      let remaining = this.targetNumber;
      const solutionCount = Math.min(Math.floor(Math.random() * 2) + 2, this.maxAddends);
      console.log('Solution count:', solutionCount);

      for (let i = 0; i < solutionCount - 1; i++) {
        const maxVal = Math.min(remaining - 1, maxNumber);
        if (maxVal <= 0) break;
        const num = Math.floor(Math.random() * maxVal) + 1;
        numbers.add(num);
        remaining -= num;
        console.log('Generated number:', num, 'Remaining:', remaining);
        await new Promise(resolve => setTimeout(resolve, 0));
      }

      if (remaining > 0) {
        numbers.add(remaining);
        console.log('Added remaining number:', remaining);
      }

      const maxAttempts = 20;
      let attempts = 0;
      
      while (numbers.size < 9 && attempts < maxAttempts) {
        const num = Math.floor(Math.random() * maxNumber) + 1;
        const previousSize = numbers.size;
        numbers.add(num);
        if (numbers.size > previousSize) {
          console.log('Filling remaining slots with number:', num);
        }
        attempts++;
        await new Promise(resolve => setTimeout(resolve, 10));
      }

      if (numbers.size < 9) {
        console.log(`Could only generate ${numbers.size} unique numbers after ${maxAttempts} attempts`);
      }

      const shuffledArray = Array.from(numbers);
      for (let i = shuffledArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
      }

      this.availableNumbers = [...shuffledArray] as [];
      console.log('Available numbers generated:', this.availableNumbers);
    },
    addNumber(number: number) {
      console.log('Adding number:', number);
      if (this.selectedNumbers.length < this.maxAddends && !this.isLoading) {
        this.selectedNumbers = [...this.selectedNumbers, number];
        this.updateTotal();
      }
    },
    removeNumber(index: number) {
      console.log('Removing number at index:', index);
      if (!this.isLoading) {
        this.selectedNumbers = this.selectedNumbers.filter((_, i) => i !== index);
        this.updateTotal();
      }
    },
    updateTotal() {
      this.currentTotal = this.selectedNumbers.reduce((sum, num) => sum + num, 0);
      console.log('Current total updated:', this.currentTotal);
      this.updateScaleRotation();
    },
    updateScaleRotation() {
      const diff = this.currentTotal - this.targetNumber;
      const maxRotation = 20;
      this.scaleRotation = Math.min(Math.max(diff * 2, -maxRotation), maxRotation);
      console.log('Scale rotation updated:', this.scaleRotation);
    },
    async checkAnswer() {
      console.log('Checking answer...');
      if (this.isLoading || this.timeLeft <= 0) return;

      this.isLoading = true;
      if (this.timerInterval) clearInterval(this.timerInterval);

      if (this.currentTotal === this.targetNumber) {
        const bonusPoints = Math.floor(this.timeLeft / 5);
        this.score += 1 + bonusPoints;
        this.correctAnswers++;
        this.feedbackType = 'success';
        console.log('Correct answer! Base point: 1, Bonus points:', bonusPoints, 'Total score:', this.score);
        this.feedbackMessage = `Correct! +1 point + ${bonusPoints} bonus points for ${this.timeLeft} seconds left!`;
        if (this.correctAnswers >= this.totalRounds) {
          this.endGame();
        } else {
          setTimeout(() => this.startNewRound(), 1500);
        }
      } else {
        this.feedbackType = 'error';
        this.feedbackMessage = this.currentTotal > this.targetNumber
          ? `Too high! ${this.currentTotal} > ${this.targetNumber}`
          : `Too low! ${this.currentTotal} < ${this.targetNumber}`;
        console.log('Incorrect answer:', this.feedbackMessage);
        setTimeout(() => this.startNewRound(), 1500);
      }
      this.isLoading = false;
    },
    resetSelection() {
      console.log('Resetting selection...');
      if (!this.isLoading) {
        this.selectedNumbers = [];
        this.currentTotal = 0;
        this.scaleRotation = 0;
        this.feedbackMessage = '';
      }
    },
    async saveGameProgress() {
      const userString = localStorage.getItem("user");
      const user = JSON.parse(userString || '') as User;
      console.log('Saving game progress...');

      try {
        const progressData = {
          user_id: user.uid,
          game_id: this.gameId,
          score: this.score,
          game_name:this.gameName
        };

        const response = await fetch("http://localhost:8000/game/progress", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(progressData),
        });

        if (response.ok) {
          const responseData = await response.json();
          console.log('Progress saved:', responseData.message);
        } else {
          const errorData = await response.json();
          console.error('Failed to save progress:', errorData.detail);
          alert("Failed to save progress: " + (errorData.detail || "Unknown error"));
        }
      } catch (error) {
        console.error("Error saving game progress:", error);
        alert("Error saving progress. Please try again.");
      }
    },
    async endGame() {
      this.feedbackType = 'success';
      this.feedbackMessage = `Game Over! Final score: ${this.score}/${this.totalRounds}`;
      console.log('Game over. Final score:', this.score);
      await this.saveGameProgress();
      setTimeout(async () => {
        alert(`Final Score: ${this.score}`);
        await this.resetGame();
      }, 1000);
    },
    async resetGame() {
      console.log('Resetting game...');
      this.isLoading = true;
      if (this.timerInterval) clearInterval(this.timerInterval);
      this.score = 0;
      this.level = 1;
      this.correctAnswers = 0;
      this.currentRound = 1;
      this.gameStarted = false; // Reset to start screen
      this.isLoading = false;
    },
  },
  beforeUnmount() {
    if (this.timerInterval) clearInterval(this.timerInterval);
  },
});
</script>

<style scoped>
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>