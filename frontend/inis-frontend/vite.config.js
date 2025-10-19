import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const isProd = mode === 'production'
  return {
    plugins: [react()],
    // Ensure assets resolve correctly when deployed at root
    base: '/',
    build: {
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: !isProd,
    },
    server: {
      port: 5173,
      strictPort: true,
    },
    preview: {
      port: 5173,
      strictPort: true,
    },
  }
})
