#!/usr/bin/env python3
"""
Render Deployment Helper

This script helps prepare your project for deployment to Render.
"""

import os
import secrets
import subprocess
import sys

def check_git_repo():
    """Check if this is a git repository."""
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        print("✅ Git repository found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Not a git repository")
        return False

def check_required_files():
    """Check if all required files exist."""
    required_files = [
        'app.py',
        'requirements.txt',
        'yelp_categories.json',
        'templates/index.html',
        'main.py',
        'yelp_api_client.py',
        'excel_generator.py',
        'config.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def generate_secret_key():
    """Generate a secure secret key."""
    return secrets.token_urlsafe(32)

def create_env_example():
    """Create an example .env file for deployment."""
    secret_key = generate_secret_key()
    
    env_content = f"""# Environment variables for deployment
# Copy this to your deployment platform's environment variables

YELP_API_KEY=your_yelp_api_key_here
SECRET_KEY={secret_key}
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env.example file")
    print(f"🔑 Generated secret key: {secret_key}")

def show_deployment_steps():
    """Show the deployment steps."""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT STEPS FOR RENDER")
    print("="*60)
    
    print("\n1. 📝 Create a Render account:")
    print("   Go to https://render.com and sign up")
    
    print("\n2. 🔗 Push to GitHub:")
    print("   git add .")
    print("   git commit -m 'Prepare for deployment'")
    print("   git push origin main")
    
    print("\n3. 🌐 Deploy on Render:")
    print("   - Click 'New +' → 'Web Service'")
    print("   - Connect your GitHub repository")
    print("   - Name: yelp-mailing-list-generator")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python app.py")
    print("   - Plan: Free")
    
    print("\n4. ⚙️ Set Environment Variables:")
    print("   - YELP_API_KEY = your actual Yelp API key")
    print("   - SECRET_KEY = the key generated above")
    
    print("\n5. 🚀 Deploy:")
    print("   - Click 'Create Web Service'")
    print("   - Wait 2-3 minutes for deployment")
    print("   - Your app will be live!")
    
    print("\n📋 Your app URL will be:")
    print("   https://your-app-name.onrender.com")
    
    print("\n🔧 Alternative platforms:")
    print("   - Railway: https://railway.app")
    print("   - PythonAnywhere: https://pythonanywhere.com")
    print("   - Vercel: https://vercel.com")

def main():
    """Main function."""
    print("🚀 Render Deployment Helper")
    print("=" * 40)
    
    # Check prerequisites
    if not check_git_repo():
        print("\n💡 To deploy, you need to:")
        print("   1. Initialize git: git init")
        print("   2. Add files: git add .")
        print("   3. Commit: git commit -m 'Initial commit'")
        print("   4. Create GitHub repository and push")
        return
    
    if not check_required_files():
        print("\n❌ Please ensure all required files are present before deploying")
        return
    
    # Create example env file
    create_env_example()
    
    # Show deployment steps
    show_deployment_steps()
    
    print("\n✅ Ready for deployment!")
    print("📖 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main() 