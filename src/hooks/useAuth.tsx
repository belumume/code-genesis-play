
import { useState, useEffect } from 'react';
import { User, Session } from '@supabase/supabase-js';
import { supabase } from '@/integrations/supabase/client';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Security: Session cleanup utility
  const cleanupAuthState = () => {
    try {
      Object.keys(localStorage).forEach((key) => {
        if (key.startsWith('supabase.auth.') || key.includes('sb-')) {
          localStorage.removeItem(key);
        }
      });
      Object.keys(sessionStorage || {}).forEach((key) => {
        if (key.startsWith('supabase.auth.') || key.includes('sb-')) {
          sessionStorage.removeItem(key);
        }
      });
    } catch (err) {
      console.warn('Auth cleanup failed:', err);
    }
  };

  useEffect(() => {
    // Set up auth state listener first
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
        setIsLoading(false);
        
        // Security: Log significant auth events (but not sensitive data)
        if (event === 'SIGNED_IN') {
          console.info('User authenticated successfully');
        } else if (event === 'SIGNED_OUT') {
          console.info('User signed out');
          cleanupAuthState();
        }
      }
    );

    // Then check for existing session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setIsLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    try {
      // Security: Clean up auth state before signing out
      cleanupAuthState();
      
      const { error } = await supabase.auth.signOut({ scope: 'global' });
      if (error) throw error;
      
      // Security: Force page reload for complete state cleanup
      window.location.href = '/auth';
    } catch (error) {
      console.error('Error signing out:', error);
      // Security: Even if signout fails, cleanup local state and redirect
      cleanupAuthState();
      window.location.href = '/auth';
    }
  };

  return {
    user,
    session,
    isLoading,
    signOut,
    isAuthenticated: !!user,
  };
}
