#!/usr/bin/env python3
"""
JobMatch Checker Setup Script
Helps configure API keys and environment settings
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("🚀 " + "="*50)
    print("   JobMatch Checker - Setup & Configuration")
    print("="*52)
    print()

def check_python():
    """Check Python version"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def setup_environment():
    """Set up virtual environment and dependencies"""
    print("\n📦 Setting up environment...")
    
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        pip_path = venv_path / "Scripts" / "pip"
    else:  # Unix/Linux/macOS
        pip_path = venv_path / "bin" / "pip"
    
    print("Installing dependencies...")
    subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
    print("✅ Dependencies installed")

def configure_api_key():
    """Configure OpenAI API key"""
    print("\n🔑 OpenAI API Key Configuration")
    print("Choose an option:")
    print("1. Enter API key now")
    print("2. Set up later (app will run in fallback mode)")
    print("3. Skip (already configured)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        api_key = input("Enter your OpenAI API key (sk-...): ").strip()
        if api_key.startswith("sk-"):
            # Create .env file
            with open(".env", "w") as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            print("✅ API key saved to .env file")
            return True
        else:
            print("❌ Invalid API key format. Should start with 'sk-'")
            return False
    
    elif choice == "2":
        print("⚠️  You can add your API key later by:")
        print("   1. Creating a .env file with: OPENAI_API_KEY=your-key")
        print("   2. Or setting environment variable: export OPENAI_API_KEY=your-key")
        return False
    
    else:
        print("✅ Skipping API key configuration")
        return False

def create_sample_files():
    """Create sample job description and CV files"""
    print("\n📄 Creating sample files...")
    
    # Sample job description
    sample_jd = """Senior Product Manager - AI/ML Products

We are seeking an experienced Senior Product Manager to lead our AI/ML product initiatives.

Responsibilities:
- Own product roadmaps and PRDs for AI-powered features
- Collaborate with ML engineers and data scientists
- Define success metrics and KPIs for ML models
- Lead cross-functional teams to deliver AI products

Requirements:
- 5+ years product management experience
- Experience with ML/AI products
- Strong analytical and technical skills
- Masters degree preferred

Location: San Francisco, CA or Remote"""

    sample_cv = """John Smith
Senior Product Manager

Experience:
Senior Product Manager | TechCorp (2020-2024)
- Led product development for ML-powered recommendation engine
- Managed cross-functional teams of 15+ engineers and data scientists
- Shipped 3 major AI features that generated $2M in revenue
- Conducted A/B testing resulting in 20% improvement in conversion

Education:
- MS Computer Science, Stanford University
- BS Engineering, UC Berkeley

Skills:
- Product Management, Machine Learning, Data Science
- A/B Testing, Python, SQL"""

    # Create samples directory
    samples_dir = Path("samples")
    samples_dir.mkdir(exist_ok=True)
    
    with open(samples_dir / "sample_job_description.txt", "w") as f:
        f.write(sample_jd)
    
    with open(samples_dir / "sample_resume.txt", "w") as f:
        f.write(sample_cv)
    
    print("✅ Sample files created in ./samples/")

def print_instructions():
    """Print usage instructions"""
    print("\n🎯 " + "="*40)
    print("   Setup Complete! Next Steps:")
    print("="*42)
    print()
    print("1. Start the application:")
    print("   source .venv/bin/activate")
    print("   uvicorn src.app:app --reload --port 8000")
    print()
    print("2. Access the application:")
    print("   🌐 Web Interface: http://localhost:8000")
    print("   📖 API Docs: http://localhost:8000/docs")
    print("   💚 Health Check: http://localhost:8000/health")
    print()
    print("3. To add OpenAI API key later:")
    print("   echo 'OPENAI_API_KEY=sk-your-key' > .env")
    print()
    print("🎉 Happy job matching!")

def main():
    print_banner()
    
    if not check_python():
        sys.exit(1)
    
    try:
        setup_environment()
        api_configured = configure_api_key()
        create_sample_files()
        print_instructions()
        
        if not api_configured:
            print("\n⚠️  Note: Running in fallback mode without OpenAI API key")
            print("   Basic functionality available, full features require API key")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
