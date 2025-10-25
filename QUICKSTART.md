# 🚀 Quick Start Guide

## Choose Your Deployment Method

### ⚡ Option 1: Railway (Recommended - 5 minutes)

**Why Railway?**
- ✅ Free tier with 500 hours/month
- ✅ Automatic HTTPS
- ✅ Auto-deploys from GitHub
- ✅ No credit card required for trial

**Steps:**

1. **Push to GitHub** (if you haven't already)
   ```bash
   # Your code is already in git!
   # Just make sure it's pushed to GitHub
   git remote add github https://github.com/YOUR_USERNAME/assistant.git
   git push github claude/ai-personal-assistant-011CUT8FEJCjgJCiaQYLsXte:main
   ```

2. **Deploy to Railway**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Login with GitHub
   - Click "Deploy from GitHub repo"
   - Select your `assistant` repository
   - Railway will auto-detect and deploy!

3. **Generate Domain**
   - Click on your deployed service
   - Go to Settings → Domains
   - Click "Generate Domain"
   - Copy your URL (e.g., `https://your-app.up.railway.app`)

4. **Configure App**
   - Visit your Railway URL
   - Click "⚙️ Settings"
   - Add your API keys (see below)
   - Click "Save Configuration"

**Done! Your app is live! 🎉**

---

### 🐳 Option 2: Docker (Local - 2 minutes)

**For testing locally before deploying:**

```bash
# Run this command:
./deploy-local.sh

# Or manually:
docker-compose up -d
```

**Access at:** http://localhost:8000

---

### 🌐 Option 3: Render (Alternative Cloud)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Render auto-detects configuration
6. Click "Create Web Service"
7. Wait for deployment
8. Visit URL and configure

---

## 🔑 Getting Your API Keys

You need **at least one** AI provider (Anthropic OR OpenAI):

### Anthropic Claude API (Recommended)

**Why Anthropic?**
- More affordable ($3 per million tokens)
- Better at following instructions
- Longer context window
- Great for personal assistants

**Get Your Key:**

1. Go to https://console.anthropic.com/
2. Click "Sign Up" or "Login"
3. Navigate to "API Keys" in the left sidebar
4. Click "Create Key"
5. Name it "Personal Assistant"
6. Copy the key (starts with `sk-ant-api-`)
7. **Save it somewhere safe!** You can only see it once

**Free Trial:** $5 credit to start

**Pricing:** ~$3 per 1M tokens (very affordable for personal use)

---

### OpenAI API (Alternative)

**Get Your Key:**

1. Go to https://platform.openai.com/
2. Sign up or login
3. Click on your profile → "View API Keys"
4. Click "Create new secret key"
5. Name it "Personal Assistant"
6. Copy the key (starts with `sk-`)
7. **Save it!** You can only see it once

**Free Trial:** $5 credit for new accounts

**Pricing:** Varies by model (~$10-30 per 1M tokens)

---

## ⚙️ Configuring Your App

Once your app is deployed:

### 1. Visit Your App URL

Railway: `https://your-app.up.railway.app`
Render: `https://your-app.onrender.com`
Local: `http://localhost:8000`

### 2. Go to Settings

Click **"⚙️ Settings"** in the top navigation bar

### 3. Enter Your API Keys

**Required (choose one or both):**
- Anthropic API Key: `sk-ant-api-xxxxx`
- OpenAI API Key: `sk-xxxxx`

**Optional (for later):**
- Gmail credentials (for email management)
- Outlook credentials (for email management)
- Google Calendar credentials
- Microsoft Calendar credentials

### 4. Generate Secret Key

Click the **"Generate"** button next to Secret Key

### 5. Save Configuration

Click **"Save Configuration"**

### 6. Test Connection

Click **"Test AI Connection"** to verify it works

**If you see "✓ Success!" you're all set!**

---

## 🎯 Start Using Your Assistant

### Chat Interface

1. Click **"Chat"** in the navigation
2. Try asking:
   - "What can you help me with?"
   - "Create a workout plan for beginners"
   - "Help me plan meals for this week"
   - "What should I prioritize today?"

### Task Management

1. Click **"Tasks"**
2. Create your first task
3. Let AI help prioritize and break it down

### Meal Planning

1. Click **"Meals"**
2. Generate a weekly meal plan
3. Track your nutrition

### Workout Planning

1. Click **"Workouts"**
2. Generate personalized workout plan
3. Log your exercises

### Schedule Optimization

1. Click **"Schedule"**
2. Let AI optimize your daily schedule
3. Find time for important tasks

---

## 💰 Cost Estimate

### Hosting
- **Railway Free Tier:** 500 hours/month (plenty for personal use)
- **Railway Paid:** $5/month if you exceed free tier
- **Render Free Tier:** 750 hours/month
- **Docker (Self-hosted):** Your server costs

### AI Usage (Anthropic Claude)
- **Light use** (5-10 queries/day): $1-3/month
- **Moderate use** (20-30 queries/day): $5-10/month
- **Heavy use** (50+ queries/day): $15-25/month

**Total for most users: $0-10/month**

---

## 🔧 Troubleshooting

### App won't deploy
- Check that all files are committed and pushed
- Review deployment logs on Railway/Render
- Ensure repository is public or Railway/Render has access

### Can't save settings
- Wait 30 seconds after deployment for database to initialize
- Try refreshing the page
- Check browser console for errors (F12)

### AI not responding
- Verify API key is correct (check for extra spaces)
- Ensure you have credits on your Anthropic/OpenAI account
- Test connection using "Test AI Connection" button

### "Not Configured" warning
- You need to add at least one AI API key
- Go to Settings and add Anthropic OR OpenAI key
- Click Save Configuration

---

## 📚 Next Steps

Once configured:

1. **Explore Features**
   - Read [docs/features.md](docs/features.md)
   - Try the chat interface
   - Create tasks and schedules

2. **Connect Integrations** (Optional)
   - Set up Gmail for email management
   - Connect Google Calendar
   - Add Outlook if needed

3. **Customize**
   - Choose default AI provider
   - Set preferences
   - Adjust settings

4. **Get Help**
   - Check [docs/deployment.md](docs/deployment.md)
   - Review [docs/api.md](docs/api.md)
   - Read [docs/setup.md](docs/setup.md)

---

## 🎉 You're All Set!

Your AI Personal Assistant is ready to help you with:
- ✅ Email management and drafting
- ✅ Calendar and scheduling
- ✅ Task prioritization
- ✅ Meal planning and nutrition
- ✅ Workout planning and fitness
- ✅ Schedule optimization
- ✅ And much more!

**Enjoy your AI assistant! 🚀**

---

## 💡 Pro Tips

1. **Use the Chat Interface** - It's the most powerful way to interact
2. **Let AI Optimize Your Schedule** - Save hours every week
3. **Track Everything** - The more data, the better AI recommendations
4. **Start Small** - Begin with one feature (like tasks) and expand
5. **Ask Questions** - The AI can help you use the app better

---

Need help? Check the docs folder or create an issue on GitHub!
