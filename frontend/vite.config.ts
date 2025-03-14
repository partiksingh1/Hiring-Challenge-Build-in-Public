import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Vite configuration
export default defineConfig({
  plugins: [vue()],
  build: {
    sourcemap: true, // Equivalent to Webpack's devtool: 'source-map'
  }
})
