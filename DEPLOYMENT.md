# Deployment Guide

This guide will help you deploy your Yelp Business Mailing List Generator to make it accessible to anyone on the internet.

## Option 1: Render (Recommended - Free)

Render is a modern cloud platform that offers free hosting for web applications.

### Steps:

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Connect Your Repository**
   - Push your code to GitHub/GitLab
   - In Render dashboard, click "New +" → "Web Service"
   - Connect your repository

3. **Configure the Service**
   - **Name**: `yelp-mailing-list-generator`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

4. **Set Environment Variables**
   - Go to Environment tab
   - Add: `YELP_API_KEY` = your Yelp API key
   - Add: `SECRET_KEY` = a random secret string

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Your app will be available at: `https://your-app-name.onrender.com`

## Option 2: Railway (Free Tier)

Railway is another excellent option for quick deployment.

### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

3. **Configure Environment**
   - Add environment variables:
     - `YELP_API_KEY`
     - `SECRET_KEY`

4. **Deploy**
   - Railway will automatically detect it's a Python app
   - Your app will be available at the provided URL

## Option 3: Heroku (Paid)

Heroku is a popular platform but now requires a paid plan.

### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set YELP_API_KEY=your_api_key
   heroku config:set SECRET_KEY=your_secret_key
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Option 4: PythonAnywhere (Free)

PythonAnywhere is great for Python web apps.

### Steps:

1. **Create Account**
   - Go to [pythonanywhere.com](https://pythonanywhere.com)
   - Sign up for free account

2. **Upload Files**
   - Upload all project files to your account
   - Or clone from GitHub

3. **Create Web App**
   - Go to Web tab
   - Click "Add a new web app"
   - Choose "Flask" and Python 3.9

4. **Configure WSGI File**
   - Edit the WSGI file to point to your app
   - Set environment variables

5. **Deploy**
   - Reload the web app
   - Your app will be at: `yourusername.pythonanywhere.com`

## Option 5: Vercel (Free)

Vercel is excellent for frontend-heavy apps.

### Steps:

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project"
   - Import your GitHub repository

3. **Configure**
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `.`
   - Install Command: `pip install -r requirements.txt`

4. **Set Environment Variables**
   - Add `YELP_API_KEY` and `SECRET_KEY`

5. **Deploy**
   - Click "Deploy"
   - Your app will be available immediately

## Environment Variables

All deployments need these environment variables:

```bash
YELP_API_KEY=your_yelp_api_key_here
SECRET_KEY=your_random_secret_key_here
```

## Security Considerations

1. **API Key Protection**: Never commit your API key to version control
2. **Rate Limiting**: Consider adding rate limiting for production use
3. **File Cleanup**: Temporary files are automatically cleaned up
4. **HTTPS**: All cloud platforms provide HTTPS by default

## Troubleshooting

### Common Issues:

1. **Port Issues**: The app uses `PORT` environment variable automatically
2. **Missing Dependencies**: Ensure `requirements.txt` is up to date
3. **API Key**: Verify your Yelp API key is valid and has remaining quota
4. **File Permissions**: Cloud platforms handle this automatically

### Testing Deployment:

1. **Health Check**: Visit `/health` endpoint
2. **Form Test**: Try generating a small mailing list
3. **Download Test**: Verify file downloads work

## Cost Comparison

| Platform | Free Tier | Paid Plans | Ease of Use |
|----------|-----------|------------|-------------|
| Render | ✅ Yes | $7/month | ⭐⭐⭐⭐⭐ |
| Railway | ✅ Yes | $5/month | ⭐⭐⭐⭐⭐ |
| Heroku | ❌ No | $7/month | ⭐⭐⭐⭐ |
| PythonAnywhere | ✅ Yes | $5/month | ⭐⭐⭐ |
| Vercel | ✅ Yes | $20/month | ⭐⭐⭐⭐ |

## Recommended for Beginners

**Render** is the best choice for beginners because:
- Completely free tier
- Easy GitHub integration
- Automatic HTTPS
- Good documentation
- Reliable uptime

## Next Steps

After deployment:

1. **Test thoroughly** with different locations and business types
2. **Monitor usage** to stay within API limits
3. **Share the URL** with your team or clients
4. **Consider scaling** if you get heavy usage

Your app will be accessible to anyone with the URL! 