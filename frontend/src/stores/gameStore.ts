import { defineStore } from 'pinia';

interface GameState {
  targetNumber: number;
  availableNumbers: number[];
  selectedNumbers: number[];
  currentTotal: number;
  scaleRotation: number;
  feedbackMessage: string;
  feedbackType: 'success' | 'error' | '';
  level: number;
  score: number;
  maxLevel: number;
  animationTimeoutId?: number;
}

export const useGameStore = defineStore('game', {
  state: (): GameState => ({
    targetNumber: 10,
    availableNumbers: [],
    selectedNumbers: [],
    currentTotal: 0,
    scaleRotation: 0,
    feedbackMessage: '',
    feedbackType: '',
    level: 1,
    score: 0,
    maxLevel: 10,
  }),

  actions: {
    initGame(level: number = 1) {
      this.level = level;
      this.targetNumber = 5 + level * 5;
      this.availableNumbers = Array.from({ length: Math.min(level * 6, 20) }, (_, i) => i + 1);
      this.selectedNumbers = [];
      this.currentTotal = 0;
      this.scaleRotation = 0;
      this.feedbackMessage = '';
      this.feedbackType = '';
    },

    addToLeft(number: number) {
      if (this.selectedNumbers.length < 3) {
        this.selectedNumbers.push(number);
        this.currentTotal = this.selectedNumbers.reduce((sum, num) => sum + num, 0);
        this.updateScaleRotation();
      }
    },

    removeFromLeft(index: number) {
      if (index >= 0 && index < this.selectedNumbers.length) {
        this.selectedNumbers.splice(index, 1);
        this.currentTotal = this.selectedNumbers.reduce((sum, num) => sum + num, 0);
        this.updateScaleRotation();
      }
    },

    updateScaleRotation() {
      const difference = this.currentTotal - this.targetNumber;
      // Scale rotation ranges from -30 to 30 degrees based on difference
      this.scaleRotation = Math.max(-30, Math.min(30, difference * 5));
    },

    checkAnswer() {
      if (this.currentTotal === this.targetNumber && this.selectedNumbers.length > 0) {
        this.score += 1;
        this.feedbackMessage = 'Correct! The numbers add up to the target!';
        this.feedbackType = 'success';
        if (this.level < this.maxLevel) {
          this.level += 1;
        }
        setTimeout(() => {
          this.initGame(this.level);
        }, 2000);
      } else {
        this.feedbackMessage = this.currentTotal > this.targetNumber 
          ? 'Too high! Try removing some numbers.'
          : 'Too low! Try adding more numbers.';
        this.feedbackType = 'error';
        setTimeout(() => {
          this.feedbackMessage = '';
          this.feedbackType = '';
        }, 2000);
      }
    },

    resetSelection() {
      this.selectedNumbers = [];
      this.currentTotal = 0;
      this.scaleRotation = 0;
      this.feedbackMessage = '';
      this.feedbackType = '';
    },
  },
});