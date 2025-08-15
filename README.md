# Resume Analyzer Backend 🧠

A powerful Flask-based backend service for analyzing resumes against job descriptions using Google's Gemini AI. This service processes resume PDFs, extracts text, communicates with Gemini AI, and delivers comprehensive analysis.

![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Gemini AI](https://img.shields.io/badge/Gemini%20AI-0.3.2-purple)

## ✨ Features

- **PDF Text Extraction**: Intelligent parsing of resume PDFs
- **Resume Analysis with Gemini AI**: Advanced AI-powered evaluation
- **Match Score Calculation**: Quantified compatibility metrics
- **ATS Compatibility Assessment**: Pass through applicant tracking systems
- **Skills Analysis**: Matching, missing, and additional skills identification
- **Section-by-Section Feedback**: Detailed insights for each resume component
- **Improvement Suggestions**: Actionable recommendations
- **Industry Insights**: Current market trends and requirements
- **Gap Analysis**: Learning paths for skill development

## 📁 Project Structure

```
backend/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── routes.py               # API endpoints
├── requirements.txt        # Dependencies
├── services/
│   └── gemini_service.py   # Gemini API integration
│   └── gemini_service_updated.py # Updated Gemini service
├── uploads/                # Directory for temporary resume uploads
├── utils/
│   ├── errors.py           # Error handling utilities
│   ├── pdf_extractor.py    # PDF text extraction utilities
│   └── response_parser.py  # Response parsing utilities
└── __pycache__/            # Python cache directory
```

## 🚀 Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer.git
   cd resume-analyzer/backend
   ```

2. **Create a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Run the application**:
   ```bash
   # Method 1: Directly with Python
   python app.py
   
   # Method 2: Using Flask CLI
   flask run
   ```

The server will start on `http://localhost:5000` by default.

## 🔧 Dependencies

Key dependencies include:

- **Flask (2.3.3)**: Lightweight WSGI web application framework
- **Flask-CORS (4.0.0)**: Extension for handling Cross-Origin Resource Sharing
- **Google Generative AI (0.3.2)**: Client library for Google's Gemini API
- **PyPDF2 (3.0.1)**: Library for PDF parsing and text extraction
- **python-dotenv (1.0.0)**: Environment variable management

## 🔌 API Documentation

### Resume Analysis

#### Full Analysis with Job Description

**Endpoint**: `POST /analyze`

**Description**: Analyzes a resume against a job description, providing comprehensive insights, matching scores, and recommendations.

**Request**:
- Content-Type: `multipart/form-data`
- Body:
  - `resume`: PDF file (required)
  - `job_description`: String (required)

**Response Example**:
```json
{
  "status": "success",
  "score": 75,
  
  "summary_insights": {
    "overall_grade": "B",
    "ats_readiness": 85,
    "competitiveness": 70,
    "top_strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "priority_actions": [
      {
        "priority": "High",
        "area": "Skills",
        "recommendation": "Add missing technical skills like X, Y, Z"
      }
    ]
  },
  
  "comprehensive_analysis": {
    "overall_score": 75,
    "detailed_metrics": {
      "relevance": {
        "score": 80,
        "details": {
          "experience_match": 85,
          "education_match": 75
        }
      },
      "ats_compatibility": {
        "score": 70,
        "details": {
          "keyword_density": 65,
          "format_score": 75
        }
      },
      "content_quality": {
        "score": 75,
        "details": {
          "clarity": 70,
          "impact": 80
        }
      },
      "skills_alignment": {
        "score": 65,
        "details": {
          "matching_skills_percentage": 65,
          "missing_critical_skills": 4
        }
      }
    },
    "strengths": ["Detailed strength 1", "Detailed strength 2"],
    "weaknesses": ["Detailed weakness 1", "Detailed weakness 2"],
    "improvement_suggestions": ["Improvement suggestion 1", "Improvement suggestion 2"]
  },
  
  "ats_analysis": {
    "score": 75,
    "format_issues": ["Issue 1", "Issue 2"],
    "keyword_match": {
      "percentage": 65,
      "matches": ["Keyword 1", "Keyword 2"],
      "missing": ["Missing keyword 1", "Missing keyword 2"]
    },
    "recommendations": ["ATS recommendation 1", "ATS recommendation 2"]
  },
  
  "skills_analysis": {
    "matching_skills": ["Skill 1", "Skill 2"],
    "missing_skills": ["Missing skill 1", "Missing skill 2"],
    "additional_skills": ["Additional skill 1"]
  },
  
  "section_feedback": {
    "contact_information": "Feedback on contact section...",
    "professional_summary": "Feedback on summary...",
    "work_experience": "Feedback on work experience...",
    "education": "Feedback on education...",
    "skills": "Feedback on skills section...",
    "projects": "Feedback on projects...",
    "certifications": "Feedback on certifications..."
  },
  
  "industry_insights": {
    "industry_trends": ["Trend 1", "Trend 2"],
    "recommendations": ["Industry recommendation 1", "Industry recommendation 2"]
  },
  
  "gap_analysis": {
    "identified_gaps": ["Gap 1", "Gap 2"],
    "learning_paths": [
      {
        "gap": "Gap 1",
        "recommendations": ["Learning recommendation 1", "Learning recommendation 2"]
      }
    ]
  }
}
```

#### Resume-Only Analysis

**Endpoint**: `POST /analyze-overall`

**Description**: Analyzes just the resume without a job description, focusing on general quality and improvements.

**Request**:
- Content-Type: `multipart/form-data`
- Body:
  - `resume`: PDF file (required)

**Response**: Similar to `/analyze` but without job-matching specific sections.

### Section Improvement

**Endpoint**: `POST /improve-section`

**Description**: Generates improved versions of a specific resume section.

**Request**:
- Content-Type: `application/json`
- Body:
  ```json
  {
    "section_type": "summary", // Options: summary, experience, skills, education, etc.
    "original_text": "Your current section text..."
  }
  ```

**Response**:
```json
{
  "status": "success",
  "original_text": "Your current section text...",
  "improved_versions": {
    "professional": {
      "text": "Improved professional version...",
      "improvement_score": 85,
      "key_changes": ["Change 1", "Change 2"]
    },
    "creative": {
      "text": "Improved creative version...",
      "improvement_score": 80,
      "key_changes": ["Change 1", "Change 2"]
    }
  },
  "general_advice": "Overall advice for this section type...",
  "ats_compatibility": {
    "score": 90,
    "suggestions": ["Suggestion 1", "Suggestion 2"]
  }
}
```

### Utility Endpoints

#### Health Check

**Endpoint**: `GET /health`

**Description**: Simple endpoint to verify the API is running.

**Response**:
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

#### Test Format

**Endpoint**: `GET /test-format`

**Description**: Returns sample analysis data for frontend development and testing.

**Response**: Same structure as the `/analyze` endpoint with sample data.

#### Test Section Improvement

**Endpoint**: `GET /test-section-improvement`

**Description**: Returns sample section improvement data for frontend development.

**Response**: Same structure as the `/improve-section` endpoint with sample data.

## 🧪 Testing

### Unit Tests

The backend includes unit tests for key functionality:

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest test_api.py

# Run with verbose output
python -m pytest -v
```

### Manual API Testing

You can use the included test script for manually testing the API:

```bash
python test_api.py path/to/your/resume.pdf [path/to/job_description.txt]
```

This will:
1. Send your resume (and optional job description) to the API
2. Save the JSON response to `api_response.json`
3. Print a summary of the response

For section improvement testing:

```bash
python test_section_improvement.py "summary" "Your section text here"
```

## 🔒 Error Handling & Validation

The API includes comprehensive error handling:

- **Request Validation**: Checks for required files/parameters and valid formats
- **File Size Limits**: Prevents excessively large file uploads (currently 10MB)
- **API Throttling**: Prevents abuse and ensures service availability
- **Graceful Degradation**: Partial results returned when possible

HTTP status codes used:
- `200` - Success
- `400` - Bad Request (client error, invalid input)
- `413` - Payload Too Large
- `415` - Unsupported Media Type
- `429` - Too Many Requests
- `500` - Server Error

Error response format:
```json
{
  "status": "error",
  "error": "Detailed error message",
  "code": "ERROR_CODE"
}
```

## 🔧 Development

### Code Organization

- **app.py**: Application factory and configuration
- **routes.py**: API endpoints and route handling
- **services/gemini_service.py**: Gemini AI integration and prompt engineering
- **utils/pdf_extractor.py**: PDF parsing and text extraction
- **utils/response_parser.py**: Formatting and processing AI responses
- **utils/errors.py**: Custom exception classes and error handling

### Adding a New Feature

1. Update the appropriate service module or create a new one
2. Add any new utility functions needed
3. Define routes in routes.py
4. Add tests for new functionality
5. Update documentation

## 🚀 Deployment

The backend can be deployed in various environments:

### Docker

A Dockerfile is provided for containerization:

```bash
docker build -t resume-analyzer-backend .
docker run -p 5000:5000 -e GOOGLE_API_KEY=your_key resume-analyzer-backend
```

### Cloud Platforms

The application is designed to work well with:
- **Heroku**: Use Procfile and runtime.txt
- **AWS Elastic Beanstalk**: Compatible with EB CLI
- **Google Cloud Run**: Works with provided Dockerfile

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Implement your changes and add tests
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

**Made with ❤️ for job seekers worldwide**
