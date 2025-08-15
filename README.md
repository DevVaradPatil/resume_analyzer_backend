# Resume Analyzer Backend

A Flask-based backend for analyzing resumes against job descriptions using Google's Gemini API.

## Features

- PDF text extraction
- Resume analysis with Google Gemini AI
- Match score calculation
- ATS compatibility assessment
- Skills analysis
- Section-by-section feedback
- Improvement suggestions
- Industry insights
- Gap analysis and learning path recommendations

## Project Structure

```
backend/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── routes.py               # API endpoints
├── requirements.txt        # Dependencies
├── services/
│   └── gemini_service.py   # Gemini API integration
└── utils/
    ├── pdf_extractor.py    # PDF text extraction utilities
    └── response_parser.py  # Response parsing utilities
```

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume-analyzer/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the backend directory with the following:
   ```
   GOOGLE_API_KEY=your_gemini_api_key
   FLASK_ENV=dev
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`.

## API Documentation

### Analyze Resume

**Endpoint**: `POST /analyze`

**Request**:
- Content-Type: `multipart/form-data`
- Body:
  - `resume`: PDF file (required)
  - `job_description`: String (required)

**Response**:
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

### Test Format Endpoint

**Endpoint**: `GET /test-format`

Returns a sample analysis result with the correct JSON structure for testing frontend compatibility.

**Response**: Same structure as the `/analyze` endpoint but with sample data.

### Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

## Testing the API

For testing without a frontend, you can use the included test script:

```bash
python test_api.py path/to/your/resume.pdf
```

The script will send your resume to the API and save the response to `api_response.json` for inspection.

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400` - Bad Request (invalid input, unsupported file type, etc.)
- `500` - Server Error (API integration issues, parsing errors, etc.)

Error responses include a descriptive message:
```json
{
  "status": "error",
  "error": "Error message details"
}
```
