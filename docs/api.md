# API Documentation

Base URL: `http://localhost:8000/api`

## Tasks API

### Get All Tasks
```
GET /tasks
Query Parameters:
  - status: pending|in_progress|completed|cancelled
  - priority: low|medium|high|urgent
  - category: string
```

### Create Task
```
POST /tasks
Body: {
  "title": "Task title",
  "description": "Task description",
  "priority": "medium",
  "category": "work",
  "due_date": "2024-12-31T10:00:00Z",
  "estimated_duration": 60
}
```

### Update Task
```
PUT /tasks/{task_id}
Body: {
  "status": "completed"
}
```

### Delete Task
```
DELETE /tasks/{task_id}
```

### AI Task Breakdown
```
POST /tasks/{task_id}/breakdown
Response: {
  "subtasks": "AI-generated subtasks"
}
```

## Email API

### Get Email Accounts
```
GET /email/accounts
```

### Connect Email Account
```
POST /email/accounts/connect
Body: {
  "email_address": "user@example.com",
  "provider": "gmail"
}
```

### Get Inbox
```
GET /email/inbox?account_id={id}&limit=50
```

### Analyze Email
```
POST /email/analyze
Body: {
  "email_content": "Email body",
  "email_metadata": {...}
}
```

### Draft Email Response
```
POST /email/draft
Body: {
  "original_email": "Original email content",
  "instructions": "Reply accepting the meeting",
  "tone": "professional"
}
```

### Send Email
```
POST /email/send
Body: {
  "account_id": 1,
  "to": "recipient@example.com",
  "subject": "Subject",
  "body": "Email body"
}
```

## Calendar API

### Get Calendar Events
```
GET /calendar/events?start_date={iso}&end_date={iso}
```

### Create Calendar Event
```
POST /calendar/events?account_id={id}
Body: {
  "title": "Meeting",
  "start_time": "2024-12-31T10:00:00Z",
  "end_time": "2024-12-31T11:00:00Z",
  "location": "Conference Room",
  "attendees": ["person@example.com"]
}
```

### Check Availability
```
GET /calendar/availability?start_time={iso}&end_time={iso}
```

### Find Available Time
```
POST /calendar/find-time
Body: {
  "duration_minutes": 60,
  "start_search": "2024-12-25T09:00:00Z",
  "end_search": "2024-12-25T17:00:00Z"
}
```

## Meals API

### Get Meals
```
GET /meals?start_date={date}&end_date={date}&meal_type=lunch
```

### Log Meal
```
POST /meals
Body: {
  "name": "Chicken Salad",
  "meal_type": "lunch",
  "date": "2024-12-25T12:00:00Z",
  "calories": 450,
  "protein": 35,
  "carbs": 30,
  "fat": 15
}
```

### Analyze Meal
```
POST /meals/analyze
Body: {
  "description": "Grilled chicken breast with quinoa and vegetables"
}
Response: {
  "analysis": "AI nutritional analysis"
}
```

### Generate Meal Plan
```
POST /meals/plans
Body: {
  "name": "Weekly Meal Plan",
  "start_date": "2024-12-25T00:00:00Z",
  "end_date": "2025-01-01T00:00:00Z",
  "dietary_restrictions": ["vegetarian"],
  "daily_calorie_target": 2000
}
```

### Get Nutrition Summary
```
GET /meals/nutrition/summary?start_date={date}&end_date={date}
```

## Workouts API

### Get Workouts
```
GET /workouts?start_date={date}&end_date={date}
```

### Log Workout
```
POST /workouts
Body: {
  "name": "Morning Run",
  "workout_type": "cardio",
  "date": "2024-12-25T06:00:00Z",
  "duration": 30,
  "calories_burned": 300
}
```

### Generate Workout Plan
```
POST /workouts/plans
Body: {
  "name": "Strength Training Plan",
  "start_date": "2024-12-25T00:00:00Z",
  "fitness_level": "intermediate",
  "goals": ["muscle_gain", "strength"],
  "constraints": {
    "days_per_week": 4,
    "session_duration": 60
  }
}
```

### Get Workout Stats
```
GET /workouts/stats/summary?start_date={date}&end_date={date}
```

### Get Workout Recommendation
```
POST /workouts/recommend
Body: {
  "current_state": {
    "energy_level": "high",
    "time_available": 45
  }
}
```

## Events API

### Get Events
```
GET /events?start_date={iso}&end_date={iso}
```

### Create Event
```
POST /events
Body: {
  "title": "Birthday Party",
  "start_time": "2024-12-31T18:00:00Z",
  "end_time": "2024-12-31T22:00:00Z",
  "location": "Home",
  "event_type": "social"
}
```

### Get Upcoming Events
```
GET /events/upcoming/next?limit=5
```

## Schedule API

### Optimize Schedule
```
POST /schedule/optimize
Body: {
  "start_date": "2024-12-25T00:00:00Z",
  "end_date": "2025-01-01T00:00:00Z",
  "work_hours_start": "09:00",
  "work_hours_end": "17:00",
  "include_tasks": true,
  "include_workouts": true,
  "include_meals": true
}
```

### Get Daily Schedule
```
GET /schedule/daily/{date}
```

### Get Weekly Schedule
```
GET /schedule/weekly?start_date={iso}
```

### Suggest Time for Task
```
POST /schedule/suggest-time
Body: {
  "task_id": 1
}
```

## Chat API

### Get Chat History
```
GET /chat/history?limit=50
```

### Send Message
```
POST /chat/message
Body: {
  "content": "What's on my schedule today?",
  "ai_provider": "anthropic"
}
```

### WebSocket Chat
```
WS /chat/ws
```

### Clear History
```
DELETE /chat/history
```

## Health Check

```
GET /health
Response: {"status": "healthy"}
```

## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.
