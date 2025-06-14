import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { env, logEnvironmentInfo } from "@/lib/env";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

// Create QueryClient with environment-based configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: env.IS_DEVELOPMENT ? 1 : 3,
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: !env.IS_DEVELOPMENT,
    },
    mutations: {
      retry: env.IS_DEVELOPMENT ? 0 : 1,
    },
  },
});

// Initialize environment logging in development
if (env.IS_DEVELOPMENT) {
  logEnvironmentInfo();
}

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
