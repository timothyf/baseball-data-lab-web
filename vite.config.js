import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],
  build: {
    lib: {
      entry: resolve(__dirname, 'frontend/main.js'),
      name: 'App',
      fileName: () => 'app.js',
      formats: ['iife']
    },
    outDir: 'frontend/dist',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        format: 'iife'
      }
    }
  }
});
