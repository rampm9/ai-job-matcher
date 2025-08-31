# 🚀 JobMatch Checker

> **AI-Powered Job Matching with Explainable Results**

A sophisticated job matching system that analyzes resumes against job descriptions using multiple scoring dimensions and provides detailed, actionable feedback with comprehensive performance monitoring.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## ✨ Features

- 🎯 **Multi-dimensional Analysis**: Skills, responsibilities, seniority, domain fit, education, location, and outcomes
- 🧠 **AI-Powered Parsing**: Uses OpenAI GPT-4o-mini for intelligent text extraction and analysis  
- 📊 **Explainable Scoring**: Detailed breakdown with improvement suggestions
- 🌐 **Modern Web Interface**: Beautiful, responsive UI built with Tailwind CSS and Alpine.js
- 🔌 **RESTful API**: Complete API with interactive documentation
- 📁 **File Upload Support**: Accept text files and resumes (PDF support planned)
- 🐳 **Docker Ready**: Easy deployment with Docker and docker-compose
- 🔒 **Secure**: Environment-based API key management
- ⏱️ **Performance Monitoring**: Built-in timing analysis and optimization
- 🔄 **Graceful Fallbacks**: Works even without OpenAI API (deterministic mode)
- 🎛️ **Mode Tracking**: Full transparency on AI vs fallback components

## 🏗️ Architecture

```
JobMatch Checker
├── 🎨 Web Interface (Tailwind + Alpine.js)
├── ⚡ FastAPI Backend with CORS & Rate Limiting
├── 🤖 OpenAI Integration (GPT-4o-mini + text-embedding-3-small)
├── 📊 Multi-dimensional Scoring Engine
├── 🔧 Configurable Weights & Thresholds
├── ⏱️ Performance Monitoring & Optimization
└── 🛡️ Robust Error Handling & Retry Logic
```

## 📋 Requirements

### System Requirements
- **Python**: 3.8+ (3.9+ recommended)
- **Memory**: 512MB+ RAM
- **Storage**: 100MB+ free space
- **Network**: Internet connection for OpenAI API

### Dependencies
```
fastapi==0.110.0
uvicorn[standard]==0.29.0
numpy==1.26.4
pydantic==2.7.1
openai==1.40.0
python-dotenv==1.0.0
python-multipart==0.0.6
jinja2==3.1.6
```

### OpenAI API Requirements
- **API Key**: Valid OpenAI API key with available credits
- **Models Used**:
  - `gpt-4o-mini`: For parsing job descriptions and resumes
  - `text-embedding-3-small`: For semantic similarity (optional, has fallback)
- **Expected Costs**: ~$0.01-0.05 per analysis (depending on content length)

## 🚦 Quick Start

### Option 1: Automated Setup
```bash
python3 setup.py
```

### Option 2: Manual Setup
```bash
# 1. Clone and navigate
cd fitscore

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# 5. Start server
uvicorn src.app:app --reload --port 8000
```

### Option 3: Docker Deployment
```bash
# Quick start with docker-compose
docker-compose up -d

# Or build manually
docker build -t jobmatch-checker .
docker run -p 8000:8000 --env-file .env jobmatch-checker
```

## 🔑 API Key Setup

### Getting an OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Create an account or sign in
3. Generate a new API key
4. Add credits to your account (minimum $5 recommended)

### Configuration
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
ENV=prod
```

**⚠️ Security Note**: Never commit your `.env` file to version control!

## 🎯 Usage & Expectations

### Web Interface
- **URL**: `http://localhost:8000`
- **Input**: Paste job description and resume text
- **Processing Time**: 6-20 seconds (depending on content length)
- **Output**: Detailed analysis with scores, explanations, and improvements

### API Endpoints
- `GET /`: Web interface
- `POST /analyze`: Analyze job match
- `POST /analyze-file`: Upload resume file
- `GET /health`: System status
- `GET /config`: Configuration info

### Performance Expectations

#### Analysis Speed
- **Short content** (< 500 chars): 3-6 seconds
- **Medium content** (500-2000 chars): 6-12 seconds  
- **Long content** (2000+ chars): 10-20 seconds
- **Very long content**: Up to 25 seconds (with timeout protection)

#### Accuracy Modes
- **AI-Powered Mode**: Variable, intelligent scores based on semantic analysis
- **Fallback Mode**: Consistent 55% scores using deterministic algorithms
- **Mixed Mode**: Some components AI-powered, others fallback



## 📊 Scoring System

### Score Components (0-100%)
1. **Skills Coverage** (25%): Required vs nice-to-have skills match
2. **Responsibilities Similarity** (25%): Semantic matching of job duties
3. **Seniority Alignment** (15%): Experience level compatibility  
4. **Domain Fit** (15%): Industry/sector alignment
5. **Education** (10%): Degree and certification requirements
6. **Location** (5%): Geographic and visa considerations
7. **Outcomes Alignment** (5%): Achievement and impact matching

### Tier Classifications
- **🔥 Excellent Fit** (80-100%): Strong match across all dimensions
- **✅ Good Fit** (65-79%): Solid match with minor gaps
- **⚠️ Medium Fit** (50-64%): Reasonable match with some concerns
- **❌ Low Fit** (< 50%): Significant gaps or misalignment

### Must-Have Gating
- Candidates missing critical requirements are capped at 45% regardless of other scores
- Clearly identified in the analysis with specific missing items

## 🔧 Configuration

### Weights Configuration (`config/weights.json`)
```json
{
  "skills_coverage": 25.0,
  "responsibilities_similarity": 25.0,
  "seniority_alignment": 15.0,
  "domain_fit": 15.0,
  "education": 10.0,
  "location": 5.0,
  "outcomes_alignment": 5.0
}
```

### Thresholds Configuration (`config/thresholds.json`)
- Semantic similarity thresholds
- Seniority level mappings
- Must-have requirement caps
- Tier boundaries

### Synonyms Configuration (`config/synonyms.json`)
- Skill name variations
- Technology aliases
- Domain terminology

## 🚀 Performance Optimization

### Built-in Optimizations
- **Content Capping**: Limits processing to most relevant items
- **Batch Processing**: Efficient API usage (when available)
- **Retry Logic**: Exponential backoff for API failures
- **Timeout Protection**: Prevents hanging requests
- **Performance Monitoring**: Detailed timing breakdown

### Timing Analysis
Every response includes performance breakdown:
```json
{
  "timings_sec": {
    "parse_jd": 2.341,
    "parse_cv": 3.127,
    "skills_score": 0.023,
    "responsibility_match": 0.156,
    "rest": 0.089,
    "total": 5.736
  }
}
```

### Performance Tuning Tips
1. **Shorter Content**: Edit down to key points for faster processing
2. **Batch Analysis**: Process multiple candidates efficiently
3. **Monitor Timing**: Use timing data to identify bottlenecks
4. **API Credits**: Ensure sufficient OpenAI credits for consistent performance

## 🛡️ Error Handling & Reliability

### Graceful Degradation
- **No API Key**: Falls back to deterministic scoring
- **API Quota Exceeded**: Switches to fallback mode automatically
- **Network Issues**: Retry with exponential backoff
- **Timeout Protection**: 25-second maximum per component

### Mode Transparency
Every response includes mode information:
```json
{
  "modes": {
    "parsing": "ai-powered",     // or "fallback"
    "embeddings": "fallback"     // or "ai-powered"
  }
}
```

### Rate Limiting
- **Built-in Protection**: 30 requests per 5 minutes per IP
- **Graceful Handling**: Clear error messages for exceeded limits

## 🧪 Testing

### Sample Data
- `samples/sample_job_description.txt`: Example job posting
- `samples/sample_resume.txt`: Example candidate resume

### Test Commands
```bash
# Health check
curl http://localhost:8000/health

# Quick analysis test
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"jd_text":"Python developer","cv_text":"Python expert"}'


```

### Expected Test Results
- **With Valid API Key**: Variable scores (20-90%), "ai-powered" modes
- **Without API Key**: Consistent 55% scores, "fallback" modes
- **Mixed Scenarios**: Partial AI functionality with clear mode indicators

## 🚨 Troubleshooting

### Common Issues

#### "Constant 55% Scores"
- **Cause**: System in fallback mode
- **Check**: API key configuration and OpenAI credits
- **Solution**: Add valid API key with available credits

#### "Slow Performance (>20s)"
- **Cause**: Long content or API latency
- **Check**: Content length and timing breakdown
- **Solution**: Edit content or check OpenAI service status

#### "Analysis Fails"
- **Cause**: Network issues or invalid API key
- **Check**: Server logs and error messages
- **Solution**: Verify API key and network connectivity

#### "Results Not Showing in Web Interface"
- **Cause**: JavaScript errors or browser issues
- **Check**: Browser console (F12) for errors
- **Solution**: Refresh page, check network requests



## 🔄 Updates & Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Monitoring
- Check `/health` endpoint regularly
- Monitor timing data for performance regression
- Watch OpenAI API usage and costs

## 📞 Support & Contributing

### Getting Help
1. Check this README for common solutions
2. Review server logs for error details
3. Test with sample data to isolate issues
4. Verify OpenAI API key and credits



### Best Practices
1. **Keep API keys secure** - never commit to version control
2. **Monitor OpenAI usage** - set up billing alerts
3. **Use content capping** - edit long documents for better performance
4. **Test fallback mode** - ensure system works without API
5. **Monitor timing data** - optimize based on performance metrics

---

**🎉 Your JobMatch Checker is ready for production use!**

*Built with ❤️ by **madebyram** using FastAPI, OpenAI, and modern web technologies.*