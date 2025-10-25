# AI Personal Assistant

A comprehensive AI-powered personal assistant that helps manage all aspects of your work and life.

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

## Setup

See [docs/setup.md](docs/setup.md) for detailed setup instructions.

## Environment Variables

Required environment variables (create `.env` file):

```
# AI APIs
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key

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
SECRET_KEY=your_secret_key
ENVIRONMENT=development
```

## Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## License

MIT License
