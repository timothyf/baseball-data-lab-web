import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import Components from 'unplugin-vue-components/vite'
import { PrimeVueResolver } from 'unplugin-vue-components/resolvers'
import AutoImport from 'unplugin-auto-import/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    plugins: [
      vue(),
      AutoImport({
        imports: ['vue', 'vue-router', 'pinia'],
        dts: 'src/auto-imports.d.ts'
      }),
      Components({
        resolvers: [
          PrimeVueResolver({
            importStyle: false,     // we’re on PrimeVue 4 (preset handles styles)
            directives: true        // auto-register directives like v-tooltip, v-ripple
          })
        ],
        dts: 'src/components.d.ts'  // (TS projects) generate typings
      }),
    ],
    define: {
      // Avoid runtime ReferenceError by replacing process.env.NODE_ENV at build time
      'process.env.NODE_ENV': JSON.stringify('production'),
      'import.meta.env.VITE_API_BASE_URL': JSON.stringify(env.VITE_API_BASE_URL || '/api'),
    },
    build: {
      lib: {
        entry: resolve(__dirname, 'src/main.js'),
        name: 'App',
        fileName: () => 'main.js',
        formats: ['iife']
      },
      outDir: '../backend/static/frontend',
      emptyOutDir: true,
      rollupOptions: {
        output: {
          format: 'iife'
        }
      }
    }
  }
});
