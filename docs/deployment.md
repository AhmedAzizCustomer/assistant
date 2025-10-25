# Deployment Guide

This guide covers multiple ways to deploy your AI Personal Assistant.

## Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)

Railway offers free tier with 500 hours/month and $5 credit.

1. **Fork or push this repository to GitHub**

2. **Go to [Railway.app](https://railway.app)** and sign up

3. **Click "New Project" → "Deploy from GitHub repo"**

4. **Select your repository**

5. **Railway will automatically detect the configuration**

6. **Once deployed, click on your service → Settings → Domains → Generate Domain**

7. **Visit the generated URL and go to Settings page to configure your API keys**

That's it! Your app is live.

### Option 2: Render

Render offers free tier with automatic SSL.

1. **Push this repository to GitHub**

2. **Go to [Render.com](https://render.com)** and sign up

3. **Click "New +" → "Web Service"**

4. **Connect your GitHub repository**

5. **Render will detect the `render.yaml` configuration**

6. **Click "Create Web Service"**

7. **Wait for deployment to complete**

8. **Visit your app URL and configure API keys in Settings**

### Option 3: Docker (Self-Hosted)

#### Using Docker Compose (Easiest)

```bash
# Clone the repository
git clone <your-repo-url>
cd assistant

# Build and run
docker-compose up -d

# Access at http://localhost:8000
```

#### Using Docker directly

```bash
# Build the image
docker build -t ai-assistant .

# Run the container
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data ai-assistant

# Access at http://localhost:8000
```

### Option 4: Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add buildpacks
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python

# Set environment variables
heroku config:set DATABASE_URL=sqlite:///./assistant.db

# Deploy
git push heroku main

# Open app
heroku open
```

### Option 5: Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm start
```

## First-Time Setup

Once your app is deployed:

1. **Visit your app URL**

2. **Click "⚙️ Settings" in the navigation**

3. **Configure at minimum:**
   - Either Anthropic API Key OR OpenAI API Key (or both)
   - Secret Key (click "Generate" button)

4. **Optional but recommended:**
   - Email credentials (Gmail/Outlook)
   - Calendar credentials (Google/Outlook)

5. **Click "Save Configuration"**

6. **Test AI connection using the "Test AI Connection" button**

7. **Start using your assistant!**

## Environment Variables

These are now configured via the web interface, but can also be set as environment variables:

### Required
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` - At least one AI provider

### Optional
- `GMAIL_CLIENT_ID` - For Gmail integration
- `GMAIL_CLIENT_SECRET` - For Gmail integration
- `OUTLOOK_CLIENT_ID` - For Outlook integration
- `OUTLOOK_CLIENT_SECRET` - For Outlook integration
- `GOOGLE_CALENDAR_CLIENT_ID` - For Google Calendar
- `GOOGLE_CALENDAR_CLIENT_SECRET` - For Google Calendar
- `DATABASE_URL` - Database connection (defaults to SQLite)
- `SECRET_KEY` - Encryption key (auto-generated if not provided)

## Getting API Keys

### Anthropic Claude (Recommended)

1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up for an account
3. Navigate to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-api-`)

**Pricing**: Pay-as-you-go, ~$3 per million tokens

### OpenAI

1. Visit [platform.openai.com](https://platform.openai.com/)
2. Sign up for an account
3. Navigate to "API Keys"
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

**Pricing**: Pay-as-you-go, varies by model

### Gmail/Google Calendar (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API and/or Google Calendar API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Configure OAuth consent screen
6. Add authorized redirect URIs:
   - `http://localhost:8000/api/email/oauth/google/callback`
   - `https://your-domain.com/api/email/oauth/google/callback`
7. Copy Client ID and Client Secret

### Outlook (Optional)

1. Go to [Azure Portal](https://portal.azure.com/)
2. Register a new application
3. Add Microsoft Graph API permissions:
   - `Mail.Read`
   - `Mail.Send`
   - `Calendars.ReadWrite`
4. Generate a client secret
5. Add redirect URIs:
   - `http://localhost:8000/api/email/oauth/outlook/callback`
   - `https://your-domain.com/api/email/oauth/outlook/callback`
6. Copy Application (client) ID and client secret

## Updating Your Deployment

### Railway
Just push to your GitHub repository - Railway auto-deploys.

### Render
Push to GitHub - Render auto-deploys.

### Docker
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Heroku
```bash
git push heroku main
```

## Backing Up Your Data

Your data is stored in SQLite database. To backup:

### Railway/Render
Use their backup features or download the data volume.

### Docker
```bash
# Backup
docker cp container-name:/app/data/assistant.db ./backup.db

# Restore
docker cp ./backup.db container-name:/app/data/assistant.db
```

### Local
Simply copy the `assistant.db` file from your backend directory.

## Troubleshooting

### App doesn't start
- Check logs for errors
- Ensure Python 3.11+ is being used
- Verify all dependencies are installed

### Can't save settings
- Check database permissions
- Ensure data directory exists and is writable

### AI not responding
- Verify API keys are correct
- Check API key has credits/quota
- Test connection using "Test AI Connection" button

### Email/Calendar not working
- Verify OAuth credentials are correct
- Check redirect URIs match exactly
- Ensure required API scopes are granted

## Performance Optimization

### For Production
1. Use PostgreSQL instead of SQLite for better concurrent access
2. Set `ENVIRONMENT=production` in settings
3. Enable caching
4. Use a CDN for frontend static files

### Scaling
- Railway and Render scale automatically
- For Docker, use Docker Swarm or Kubernetes
- Consider separating frontend and backend services

## Security Best Practices

1. **Always use HTTPS in production** (Railway/Render provide this automatically)
2. **Generate a strong secret key** (use the Generate button in Settings)
3. **Keep API keys secure** - never commit them to Git
4. **Regularly update dependencies**
5. **Use environment-specific settings**
6. **Enable authentication** (future feature)

## Cost Estimation

### Hosting
- **Railway**: Free tier (500 hrs/month) or $5/month
- **Render**: Free tier (750 hrs/month) or $7/month
- **Heroku**: $7/month minimum
- **Self-hosted**: Your server costs

### AI API Costs (approximate)
- **Anthropic Claude**: $3-15 per million tokens
- **OpenAI GPT-4**: $10-30 per million tokens
- **Typical usage**: $5-20/month for personal use

### Total Estimated Cost
- **Minimum**: $0-5/month (free hosting + minimal AI usage)
- **Typical**: $10-25/month (paid hosting + moderate AI usage)
- **Heavy use**: $30-50/month (paid hosting + heavy AI usage)

## Support

For issues or questions:
1. Check the documentation in `/docs`
2. Review error logs
3. Open an issue on GitHub
4. Check API provider status pages
