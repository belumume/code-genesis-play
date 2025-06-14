# Environment Setup Guide

This guide explains how to set up environment variables for the AI Genesis Engine project.

## Quick Start

1. **Copy the environment template:**
   ```bash
   cp env.template .env
   ```

2. **Fill in the required values** in your `.env` file (see sections below)

3. **Start the development server:**
   ```bash
   npm run dev
   ```

## Required Environment Variables

These variables are **required** for the application to function properly:

### Supabase Configuration

```bash
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

**How to get these values:**
1. Go to your [Supabase dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to Settings > API
4. Copy the "Project URL" and "Project API keys" (anon/public key)

### AI Services

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**How to get this:**
1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Generate an API key in your account settings
3. This is used for AI-powered game generation

## Optional Environment Variables

### Development Settings

```bash
VITE_DEV_SERVER_PORT=8080
VITE_DEV_SERVER_HOST=localhost
VITE_API_BASE_URL=http://localhost:8080/api
```

### Feature Flags

Enable or disable specific features:

```bash
VITE_ENABLE_AI_GENERATION=true
VITE_ENABLE_GAME_PREVIEW=true
VITE_ENABLE_REAL_TIME_UPDATES=true
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG_MODE=false
```

### Security (Production)

```bash
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
JWT_SECRET=your_jwt_secret_minimum_32_characters
ENCRYPTION_KEY=your_encryption_key_minimum_32_characters
```

### Monitoring (Optional)

```bash
SENTRY_DSN=your_sentry_dsn_here
VITE_SENTRY_DSN=your_sentry_dsn_here
```

## Environment Files

The project uses different environment files for different purposes:

- **`.env`** - Your local development environment (never commit this!)
- **`env.template`** - Template with all available variables and documentation
- **`.env.local`** - Local overrides (also never commit)
- **`.env.production`** - Production-specific variables (if needed)

## Environment Variable Prefixes

Due to Vite's security model:

- **`VITE_`** prefixed variables are exposed to the browser/client-side code
- **Non-prefixed** variables are only available on the server-side (Node.js/Python)

## Validation and Error Handling

The application automatically validates required environment variables on startup:

- **Missing required variables** will show helpful error messages
- **Invalid values** (e.g., invalid URLs, malformed keys) will be caught early
- **Development mode** provides additional debugging information

## Production Deployment

For production deployments:

1. **Never commit `.env` files** with real credentials
2. **Use your platform's environment variable system:**
   - Vercel: Environment Variables in dashboard
   - Netlify: Site settings > Environment variables
   - Railway: Variables tab in your project
   - Docker: Use `--env-file` or docker-compose environment sections

3. **Set `NODE_ENV=production`** in your production environment

## Troubleshooting

### Common Issues

**"Missing VITE_SUPABASE_URL environment variable"**
- Make sure you've created a `.env` file from the template
- Check that the variable name is spelled correctly
- Ensure there are no spaces around the `=` sign

**"Supabase client initialization failed"**
- Verify your Supabase URL and API key are correct
- Check that your Supabase project is active
- Make sure the API key has the correct permissions

**"ANTHROPIC_API_KEY not found"**
- This variable is required for AI features
- Get your API key from the Anthropic Console
- Make sure it's not prefixed with `VITE_` (it's server-side only)

### Debug Mode

Enable debug mode for additional logging:

```bash
VITE_ENABLE_DEBUG_MODE=true
VITE_LOG_LEVEL=debug
```

### Environment Validation

The application will log environment configuration in development mode. Check the browser console for:

```
🌍 Environment Configuration
Mode: development
App Title: AI Genesis Engine
Features: { AI_GENERATION: true, ... }
```

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use different API keys** for development and production
3. **Rotate API keys regularly**
4. **Use service role keys sparingly** and only on the server-side
5. **Enable RLS (Row Level Security)** in Supabase for production
6. **Monitor API usage** to detect unauthorized access

## Getting Help

If you're having trouble with environment setup:

1. Check the browser console for error messages
2. Verify all required variables are set in your `.env` file
3. Compare your `.env` file with `env.template`
4. Check the network tab for failed API requests
5. Enable debug mode for more detailed logging

## Example .env File

Here's a minimal `.env` file to get started:

```bash
# Basic configuration
NODE_ENV=development
VITE_APP_TITLE="My AI Genesis Engine"

# Supabase (required)
VITE_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# AI Services (required for generation features)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Feature flags
VITE_ENABLE_DEBUG_MODE=true
```

Copy this structure and fill in your actual values to get started quickly. 