import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  envDir: path.resolve(__dirname, "../../infra"),
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true
    }
  }
})
