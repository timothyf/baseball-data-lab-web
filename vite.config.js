import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
  plugins: [vue()],
  define: {
    // Avoid runtime ReferenceError by replacing process.env.NODE_ENV at build time
    'process.env.NODE_ENV': JSON.stringify('production')
  },
  build: {
    lib: {
      entry: resolve(__dirname, 'frontend/main.js'),
      name: 'App',
      fileName: () => 'main.js',
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
