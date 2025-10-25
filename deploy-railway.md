# 🚂 Deploy to Railway - Step by Step

## What You'll Need
- GitHub account
- Anthropic or OpenAI API key
- 5 minutes

## Step-by-Step Instructions

### 1. Get Your Repository on GitHub

Your code is already in Git. If it's not on GitHub yet:

```bash
# Create a new repository on GitHub first, then:
git remote add github https://github.com/YOUR_USERNAME/assistant.git
git push github claude/ai-personal-assistant-011CUT8FEJCjgJCiaQYLsXte:main
```

### 2. Open Railway

Go to: **https://railway.app**

Click: **"Start a New Project"**

### 3. Login with GitHub

Click: **"Login with GitHub"**

Authorize Railway to access your repositories

### 4. Deploy from GitHub

Click: **"Deploy from GitHub repo"**

Select: **"assistant"** (or whatever you named your repo)

Railway will:
- ✅ Detect the Dockerfile
- ✅ Detect railway.json configuration
- ✅ Start building automatically
- ✅ Deploy when ready

⏱️ **This takes 3-5 minutes**

### 5. Watch the Build

You'll see:
```
Building...
Deploying...
Running...
```

When you see **"Running"** with a green dot ✅ - you're deployed!

### 6. Generate Your URL

Click on your deployed service

Go to: **Settings** tab

Scroll to: **Domains** section

Click: **"Generate Domain"**

You'll get a URL like:
```
https://ai-personal-assistant-production.up.railway.app
```

### 7. Visit Your App

Click on your generated domain

You should see:
```
AI Personal Assistant
[Dashboard] [Tasks] [Calendar] ... [Settings]
```

⚠️ You'll see a warning: **"Not Configured"** - This is normal!

### 8. Configure API Keys

Click: **"⚙️ Settings"** in the navigation

Scroll to: **"🤖 AI Configuration"**

#### Option A: Anthropic (Recommended)

1. Go to https://console.anthropic.com/
2. Create account / Login
3. Click "API Keys" in sidebar
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-api-`)
6. Paste into "Anthropic API Key" field in your app

#### Option B: OpenAI

1. Go to https://platform.openai.com/
2. Login / Signup
3. Go to "API Keys"
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Paste into "OpenAI API Key" field

### 9. Generate Secret Key

Scroll to: **"⚙️ Advanced Settings"**

Click: **"Generate"** button next to "Secret Key"

A random secure key will be created automatically

### 10. Save Configuration

Scroll down and click: **"Save Configuration"**

You should see: ✅ **"Settings saved successfully!"**

### 11. Test AI Connection

Click the button: **"Test AI Connection"**

If successful, you'll see:
```
✓ Success!
AI connection successful
Response: Hello
```

### 12. Start Using Your Assistant!

Click: **"Dashboard"**

Try:
- Creating a task
- Chatting with AI
- Generating a meal plan
- Optimizing your schedule

## 🎉 You're Done!

Your AI Personal Assistant is now live at:
```
https://your-app.up.railway.app
```

## 📊 Monitor Your App

### View Logs
In Railway dashboard:
- Click on your service
- Click "Deployments" tab
- Click on latest deployment
- Click "View Logs"

### Check Usage
Railway free tier includes:
- ✅ 500 execution hours per month
- ✅ $5 credit
- ✅ Automatic HTTPS
- ✅ Auto-deploy on git push

### Update Your App
Simply push to your GitHub repository:
```bash
git add .
git commit -m "Update app"
git push github main
```

Railway will auto-deploy the changes!

## 🆘 Troubleshooting

### Build Failed
- Check Railway logs
- Ensure Dockerfile is in repository root
- Verify all files are committed

### App Shows "Application Error"
- Wait 1-2 minutes for full startup
- Check logs for specific errors
- Ensure database initialized (happens automatically)

### Can't Save Settings
- Refresh the page
- Clear browser cache
- Check browser console (F12) for errors

### AI Not Responding
- Verify API key is correct (no extra spaces)
- Ensure you have credits on Anthropic/OpenAI account
- Check API key permissions

## 💰 Costs

### Railway
- **Free Tier**: 500 hours/month + $5 credit
- **After free tier**: ~$5/month
- **Hobby Plan**: $5/month

### Anthropic Claude
- **Free**: $5 credit for new accounts
- **Cost**: ~$3 per 1M tokens
- **Personal use**: Usually $2-10/month

### Total
**Most users: $0-10/month**

## 🔄 Next Steps

1. **Explore Features**: Try chat, tasks, meals, workouts
2. **Add Integrations**: Connect Gmail, Google Calendar (optional)
3. **Invite Others**: Share your URL (add auth in future)
4. **Customize**: Adjust AI model, preferences

## 🎯 Pro Tips

1. Use chat interface for complex requests
2. Railway auto-deploys on git push
3. Check logs if something seems wrong
4. Keep API keys secure
5. Monitor Railway usage dashboard

---

**Need help?** Check [QUICKSTART.md](QUICKSTART.md) or [docs/deployment.md](docs/deployment.md)
