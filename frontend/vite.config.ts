import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: process.env.PYSTARTER_BACKEND_URL || 'http://localhost:8002',
        changeOrigin: true,
      },
    },
  },
})
