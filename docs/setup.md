# Setup Guide

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL database (cloud-hosted recommended)
- API keys for Anthropic Claude and OpenAI

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```
# AI APIs
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# Email Integration
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
OUTLOOK_CLIENT_ID=your_outlook_client_id
OUTLOOK_CLIENT_SECRET=your_outlook_client_secret

# Calendar Integration
GOOGLE_CALENDAR_CLIENT_ID=your_google_calendar_client_id
GOOGLE_CALENDAR_CLIENT_SECRET=your_google_calendar_client_secret

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# App Config
SECRET_KEY=generate_a_random_secret_key
ENVIRONMENT=development
```

### 3. Set Up Database

```bash
# Create database tables
python -c "from backend.src.storage.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 4. Run Backend Server

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Frontend

The frontend is configured to proxy API requests to `http://localhost:8000` (see `package.json`).

### 3. Run Frontend

```bash
npm start
```

The app will open at `http://localhost:3000`

## Getting API Keys

### Anthropic Claude API

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Generate a new API key

### OpenAI API

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new secret key

### Gmail API

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs

### Outlook/Microsoft Graph API

1. Go to https://portal.azure.com/
2. Register a new application
3. Add Microsoft Graph permissions
4. Generate client secret
5. Configure redirect URIs

### Google Calendar API

1. Same Google Cloud project as Gmail
2. Enable Google Calendar API
3. Use same OAuth 2.0 credentials

## Cloud Database Setup

### PostgreSQL on Heroku

```bash
heroku addons:create heroku-postgresql:mini
heroku config:get DATABASE_URL
```

### PostgreSQL on AWS RDS

1. Create PostgreSQL instance on AWS RDS
2. Configure security groups
3. Get connection string

### PostgreSQL on Google Cloud SQL

1. Create PostgreSQL instance
2. Configure Cloud SQL Proxy
3. Get connection details

## Production Deployment

### Backend (Heroku)

```bash
heroku create your-app-name
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
# ... set other config vars
git push heroku main
```

### Frontend (Vercel)

```bash
cd frontend
vercel
```

Or use Netlify:

```bash
cd frontend
npm run build
netlify deploy --prod --dir=build
```

## Troubleshooting

### Database Connection Issues

- Check DATABASE_URL format
- Ensure database server is accessible
- Verify credentials

### API Key Issues

- Verify keys are correctly set in .env
- Check for trailing spaces
- Ensure keys have proper permissions

### CORS Issues

- Update FRONTEND_URL in .env
- Check CORS middleware configuration

### OAuth Issues

- Verify redirect URIs match exactly
- Check client ID and secret
- Ensure required scopes are configured

## Next Steps

After setup, you can:

1. Connect your email accounts via the Email page
2. Connect your calendars via the Calendar page
3. Start chatting with the AI assistant
4. Create tasks and let AI help optimize your schedule
5. Generate meal and workout plans
