<template>
  <div class="py-12">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold text-black mb-6">Balance Scale Addition Game</h1>
      
      <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
        <div class="flex flex-col md:flex-row items-center gap-8">
          <div class="w-full md:w-1/2">
            <img 
              src="/gameLogo.jpeg" 
              alt="Balance Scale Game" 
              class="rounded-lg shadow-md"
            />
          </div>
          <div class="w-full md:w-1/2 text-left">
            <h2 class="text-2xl font-bold text-black mb-4">Learn Addition with Visual Intuition</h2>
            <p class="text-gray-700 mb-6">
              Our balance scale game makes learning addition fun and intuitive! 
              Place numbers on each side of the scale and see it tip in real-time. 
              When you get the sums equal, the scale balances perfectly!
            </p>
            <div class="space-x-4">
              <!-- <router-link 
                to="/dashboard" 
                class="inline-block bg-black hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-full transition-colors shadow-md"
              >
                Start Playing
              </router-link> -->
              <router-link 
                to="/login" 
                class="inline-block bg-white hover:bg-gray-100 text-indigo-600 font-bold py-2 px-6 rounded-full border border-indigo-600 transition-colors shadow-md"
              >
                Sign In
              </router-link>
              <router-link 
                to="/register" 
                class="inline-block bg-white hover:bg-gray-100 text-indigo-600 font-bold py-2 px-6 rounded-full border border-indigo-600 transition-colors shadow-md"
              >
                Sign Up
              </router-link>
            </div>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="text-indigo-600 text-4xl mb-4">🧩</div>
          <h3 class="text-xl font-bold mb-2">Visual Learning</h3>
          <p class="text-gray-600">
            See addition in action with our interactive balance scale that gives immediate visual feedback!
          </p>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="text-indigo-600 text-4xl mb-4">🏆</div>
          <h3 class="text-xl font-bold mb-2">Level Progression</h3>
          <p class="text-gray-600">
            Start with simple additions and progress to more challenging equations as you improve!
          </p>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="text-indigo-600 text-4xl mb-4">📊</div>
          <h3 class="text-xl font-bold mb-2">Track Progress</h3>
          <p class="text-gray-600">
            Track your learning journey with detailed statistics and performance metrics!
          </p>
        </div>
      </div>
    </div>
  </div>
</template>