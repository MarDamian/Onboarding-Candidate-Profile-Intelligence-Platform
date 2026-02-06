import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import tailwindcss from '@tailwindcss/vite'
import path from "path";

 
export default defineConfig({
  plugins: [react(),tailwindcss()],
  /**envDir: path.resolve(__dirname, "../../"),*/
  server: {
    host: true,
    port: 5173,
    watch: {
      usePolling: true
    }
  }
})
