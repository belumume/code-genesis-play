
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.7.1'

// Secure CORS headers - only allow specific origins
const getAllowedOrigins = () => {
  const origins = [
    'https://code-genesis-play.lovable.app',
    'http://localhost:8080',
    'http://127.0.0.1:8080'
  ];
  
  // Add custom frontend URL if configured
  const customOrigin = Deno.env.get('FRONTEND_URL');
  if (customOrigin) {
    origins.push(customOrigin);
  }
  
  return origins;
};

const getCorsHeaders = (origin: string | null) => {
  const allowedOrigins = getAllowedOrigins();
  const allowedOrigin = origin && allowedOrigins.includes(origin) ? origin : allowedOrigins[0];
  
  return {
    'Access-Control-Allow-Origin': allowedOrigin,
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Credentials': 'true',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
  };
};

// Rate limiting storage
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();
const RATE_LIMIT_WINDOW = 60000; // 1 minute
const RATE_LIMIT_MAX_REQUESTS = 10;

const checkRateLimit = (identifier: string): boolean => {
  const now = Date.now();
  const userLimit = rateLimitMap.get(identifier);
  
  if (!userLimit || now > userLimit.resetTime) {
    rateLimitMap.set(identifier, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return true;
  }
  
  if (userLimit.count >= RATE_LIMIT_MAX_REQUESTS) {
    return false;
  }
  
  userLimit.count++;
  return true;
};

// Input validation and sanitization
const validateAndSanitizeInput = (names: unknown): string[] => {
  if (!Array.isArray(names)) {
    throw new Error('Names must be an array');
  }
  
  if (names.length === 0) {
    throw new Error('Names array cannot be empty');
  }
  
  if (names.length > 10) {
    throw new Error('Too many secrets requested');
  }
  
  const validNames: string[] = [];
  const allowedSecretPattern = /^[A-Z_][A-Z0-9_]*$/;
  
  for (const name of names) {
    if (typeof name !== 'string') {
      throw new Error('All names must be strings');
    }
    
    const sanitizedName = name.trim().toUpperCase();
    
    if (!allowedSecretPattern.test(sanitizedName)) {
      throw new Error(`Invalid secret name format: ${sanitizedName}`);
    }
    
    if (sanitizedName.length > 100) {
      throw new Error('Secret name too long');
    }
    
    validNames.push(sanitizedName);
  }
  
  return validNames;
};

serve(async (req) => {
  const origin = req.headers.get('Origin');
  const corsHeaders = getCorsHeaders(origin);
  
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }
  
  try {
    // Rate limiting based on IP
    const clientIP = req.headers.get('x-forwarded-for') || 
                     req.headers.get('cf-connecting-ip') || 
                     'unknown';
    
    if (!checkRateLimit(clientIP)) {
      return new Response(
        JSON.stringify({ error: 'Rate limit exceeded' }),
        { 
          status: 429, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }
    
    // Verify authentication
    const authHeader = req.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return new Response(
        JSON.stringify({ error: 'Authorization header required' }),
        { 
          status: 401, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }
    
    // Create authenticated Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: authHeader },
        },
      }
    );
    
    // Verify the user is authenticated
    const { data: { user }, error: authError } = await supabaseClient.auth.getUser();
    
    if (authError || !user) {
      return new Response(
        JSON.stringify({ error: 'Invalid authentication' }),
        { 
          status: 401, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }
    
    // Rate limiting per user
    if (!checkRateLimit(user.id)) {
      return new Response(
        JSON.stringify({ error: 'User rate limit exceeded' }),
        { 
          status: 429, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }
    
    // Parse and validate request body
    let requestData;
    try {
      const text = await req.text();
      requestData = JSON.parse(text);
    } catch {
      return new Response(
        JSON.stringify({ error: 'Invalid JSON in request body' }),
        { 
          status: 400, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      );
    }
    
    // Validate and sanitize input
    const validNames = validateAndSanitizeInput(requestData.names);
    
    const secrets: Record<string, string> = {};
    
    for (const name of validNames) {
      const value = Deno.env.get(name);
      if (value) {
        secrets[name] = value;
      }
    }
    
    return new Response(
      JSON.stringify(secrets),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );
    
  } catch (error) {
    console.error('Error in get-secret function:', error);
    
    // Sanitize error message to prevent information disclosure
    const sanitizedError = error instanceof Error && error.message.includes('Invalid') 
      ? error.message 
      : 'Internal server error';
    
    return new Response(
      JSON.stringify({ error: sanitizedError }),
      { 
        status: error instanceof Error && error.message.includes('Invalid') ? 400 : 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    );
  }
});
