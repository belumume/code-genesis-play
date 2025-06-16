
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '');
  
  const isDevelopment = mode === 'development';
  const isProduction = mode === 'production';
  
  return {
    server: {
      // Security: Required port configuration for Lovable platform
      port: 8080,
      host: "0.0.0.0", // Changed from "::1" to "0.0.0.0" for IPv4 compatibility
      open: isDevelopment, // Auto-open browser in development
      cors: true,
      // Security: Additional server hardening
      headers: {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
      },
    },
    
    plugins: [
      react(),
      // Only use component tagger in development mode
      isDevelopment && componentTagger(),
    ].filter(Boolean),
    
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    
    // Define global constants that can be replaced at build time
    define: {
      __APP_VERSION__: JSON.stringify(env.VITE_APP_VERSION || '1.0.0'),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    },
    
    // Build optimization
    build: {
      target: 'es2020',
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
            ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
            supabase: ['@supabase/supabase-js'],
          },
        },
      },
      // Generate source maps in development but not in production (for security)
      sourcemap: isDevelopment,
    },
    
    // Optimize dependencies
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        '@supabase/supabase-js',
        '@tanstack/react-query',
      ],
    },
    
    // Preview server configuration (for production builds)
    preview: {
      port: 8081,
      host: "0.0.0.0", // Changed from "::1" to "0.0.0.0" for IPv4 compatibility
      // Security: Preview server headers
      headers: {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
      },
    },
    
    // Environment variables configuration
    envPrefix: ['VITE_'], // Only expose VITE_ prefixed vars to client
  };
});
