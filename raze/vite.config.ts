import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => ({
  plugins: [
    react(mode === 'test' ? {} : { babel: { plugins: ['babel-plugin-react-compiler'] } }),
    ...(mode !== 'test' ? [tailwindcss()] : []),
  ],
  test: {
    environment: 'happy-dom',
    globals: true,
    setupFiles: './src/test/setup.ts',
    css: false,
  },
}))
