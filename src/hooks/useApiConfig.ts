
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
    apiBaseUrl: 'https://ai-genesis-engine.onrender.com', // Default to production
    wsBaseUrl: 'wss://ai-genesis-engine.onrender.com', // Default to production
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    async function fetchConfig() {
      try {
        // Default to production URLs - these will work immediately
        const productionConfig = {
          apiBaseUrl: 'https://ai-genesis-engine.onrender.com',
          wsBaseUrl: 'wss://ai-genesis-engine.onrender.com',
          isLoading: false,
          error: null,
        };

        // Try to get custom config from edge function, but don't block if it fails
        try {
          const { data: { session } } = await supabase.auth.getSession();
          
          if (session) {
            const { data, error } = await supabase.functions.invoke('get-secret', {
              body: { names: ['VITE_API_BASE_URL', 'VITE_WS_BASE_URL'] },
              headers: {
                Authorization: `Bearer ${session.access_token}`,
              },
            });

            if (!error && data) {
              const apiBaseUrl = data.VITE_API_BASE_URL || productionConfig.apiBaseUrl;
              const wsBaseUrl = data.VITE_WS_BASE_URL || productionConfig.wsBaseUrl;

              // Validate URLs before using them
              try {
                new URL(apiBaseUrl);
                new URL(wsBaseUrl.replace('wss://', 'https://').replace('ws://', 'http://'));
                
                setConfig({
                  apiBaseUrl,
                  wsBaseUrl,
                  isLoading: false,
                  error: null,
                });
                return;
              } catch (urlError) {
                console.warn('Invalid API URLs received, using production defaults');
              }
            }
          }
        } catch (err) {
          console.warn('Failed to fetch custom API config, using production URLs:', err);
        }

        // Always fall back to production config
        setConfig(productionConfig);
        
      } catch (err) {
        console.warn('API config setup failed, using production defaults:', err);
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
