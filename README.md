# AI Personal Assistant

A comprehensive AI-powered personal assistant that helps manage all aspects of your work and life.

## 🚀 Quick Start

**Deploy in 2 minutes:**

1. Click to deploy on [Railway](https://railway.app) or [Render](https://render.com)
2. Once deployed, visit your app URL
3. Click "⚙️ Settings" and enter your API keys through the web interface
4. Start using your AI assistant!

**No manual configuration needed!** Everything is configured through the web interface.

## Features

### Email Management
- Gmail and Outlook integration
- Smart email summarization and prioritization
- AI-powered draft responses
- Email categorization and filtering

### Calendar & Meetings
- Google Calendar and Outlook Calendar sync
- Smart scheduling with conflict detection
- Meeting preparation and summaries
- Automated reminders

### Task Management
- Intelligent task prioritization
- Deadline tracking and reminders
- Task categorization (work/personal)
- AI-powered task breakdown

### Schedule Planning
- Optimal schedule generation
- Time blocking recommendations
- Work-life balance optimization
- Smart task scheduling based on priorities

### Meal Planning
- Personalized meal plans
- Nutritional tracking and analysis
- Recipe suggestions
- Grocery list generation
- Dietary preferences and restrictions

### Diet Tracking
- Meal logging and calorie tracking
- Nutritional analysis
- Progress tracking
- AI-powered dietary recommendations

### Exercise & Fitness
- Workout planning and tracking
- Exercise recommendations
- Progress monitoring
- Integration with fitness goals

### Events Tracking
- Personal and professional events
- Event reminders and preparation
- Travel planning assistance

## Architecture

```
ai-personal-assistant/
├── backend/               # Python FastAPI backend
│   ├── src/
│   │   ├── core/         # Core AI engine and config
│   │   ├── modules/      # Feature modules
│   │   ├── integrations/ # Third-party API integrations
│   │   ├── storage/      # Database models and operations
│   │   └── api/          # REST API endpoints
│   ├── tests/
│   └── requirements.txt
├── frontend/             # React web application
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── utils/        # Utility functions
│   └── package.json
└── docs/                 # Documentation
```

## Technology Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Frontend**: React 18+, TypeScript, Tailwind CSS
- **AI**: Anthropic Claude API, OpenAI API
- **Database**: PostgreSQL (cloud-ready)
- **APIs**: Gmail API, Microsoft Graph API, Google Calendar API

## Deployment

### Option 1: One-Click Deploy (Recommended)

Deploy to cloud platforms with one click:

- **Railway**: Push to GitHub → Connect to Railway → Auto-deploy
- **Render**: Push to GitHub → Connect to Render → Auto-deploy
- **Heroku**: `heroku create && git push heroku main`

See [docs/deployment.md](docs/deployment.md) for detailed deployment instructions.

### Option 2: Docker

```bash
docker-compose up -d
```

Access at http://localhost:8000

### Option 3: Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## Configuration

**All configuration is done through the web interface!**

1. Visit your deployed app URL
2. Click "⚙️ Settings" in the navigation
3. Enter your API keys and credentials:
   - **Required**: Anthropic API key OR OpenAI API key
   - **Optional**: Email and calendar credentials for integrations
4. Click "Save Configuration"
5. Test your AI connection
6. Start using your assistant!

### Getting API Keys

- **Anthropic**: [console.anthropic.com](https://console.anthropic.com/) (Recommended)
- **OpenAI**: [platform.openai.com](https://platform.openai.com/)

See [docs/deployment.md](docs/deployment.md) for detailed API key setup instructions.

## Documentation

- **[Setup Guide](docs/setup.md)** - Detailed setup instructions
- **[Deployment Guide](docs/deployment.md)** - How to deploy to various platforms
- **[API Documentation](docs/api.md)** - Complete API reference
- **[Features Guide](docs/features.md)** - How to use all features

## License

MIT License
