import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      // Proxy all /api requests to the backend during development.
      // In production, Nginx handles this routing.
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path, // keep /api prefix – backend expects it
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        // Split large libraries into separate chunks for better caching.
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
})
