import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: { port: 3000 },
  build: {
    sourcemap: true, // ✅ Включаем sourcemaps
    minify: false, // ✅ Отключаем minify для читаемого кода
  },
  define: {
    "process.env.NODE_ENV": JSON.stringify("development"),
    "import.meta.env.VITE_API_URL": JSON.stringify("http://localhost:8000"),
    "import.meta.env.VITE_DEBUG_MODE": JSON.stringify("on"),
  },
});
