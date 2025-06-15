
import { useState, useEffect } from 'react';
import { supabase } from '@/integrations/supabase/client';

interface ApiConfig {
  apiBaseUrl: string;
  wsBaseUrl: string;
  isLoading: boolean;
  error: string | null;
}

export function useApiConfig(): ApiConfig {
  const [config, setConfig] = useState<ApiConfig>({
    apiBaseUrl: 'http://localhost:8000', // fallback
    wsBaseUrl: 'ws://localhost:8000', // fallback
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    async function fetchConfig() {
      try {
        // Get the current session for authentication
        const { data: { session } } = await supabase.auth.getSession();
        
        if (!session) {
          // If no session, use fallback URLs
          setConfig({
            apiBaseUrl: 'https://ai-genesis-engine.onrender.com',
            wsBaseUrl: 'wss://ai-genesis-engine.onrender.com',
            isLoading: false,
            error: null,
          });
          return;
        }

        // Try to get the API URLs from Supabase secrets via edge function
        const { data, error } = await supabase.functions.invoke('get-secret', {
          body: { names: ['VITE_API_BASE_URL', 'VITE_WS_BASE_URL'] },
          headers: {
            Authorization: `Bearer ${session.access_token}`,
          },
        });

        if (error) throw error;

        const apiBaseUrl = data?.VITE_API_BASE_URL || 'https://ai-genesis-engine.onrender.com';
        const wsBaseUrl = data?.VITE_WS_BASE_URL || 'wss://ai-genesis-engine.onrender.com';

        setConfig({
          apiBaseUrl,
          wsBaseUrl,
          isLoading: false,
          error: null,
        });
      } catch (err) {
        console.warn('Failed to fetch API config from secrets, using deployed URLs:', err);
        // Fallback to the deployed URLs
        setConfig({
          apiBaseUrl: 'https://ai-genesis-engine.onrender.com',
          wsBaseUrl: 'wss://ai-genesis-engine.onrender.com',
          isLoading: false,
          error: null,
        });
      }
    }

    fetchConfig();
  }, []);

  return config;
}
