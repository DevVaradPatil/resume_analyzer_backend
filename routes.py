from flask import Blueprint, request, jsonify, make_response
import logging
import os

from services.gemini_service import analyze_resume_with_gemini, improve_resume_section_with_gemini, analyze_resume_overall_with_gemini
from utils.pdf_extractor import extract_text_from_pdf
from utils.response_parser import parse_gemini_response
from utils.errors import BadRequestError, ServerError
from utils.cors_helper import get_cors_origins

# Create a Blueprint for API routes
api = Blueprint('api', __name__)
    
# Debug endpoint for CORS verification
@api.route('/debug/cors', methods=['GET'])
def debug_cors():
    """Debug endpoint to check CORS settings"""
    cors_origins = get_cors_origins()
    request_origin = request.headers.get('Origin', 'No origin header')
    
    # Check response headers (these will be added by Flask-CORS)
    response = make_response(jsonify({
        "status": "success",
        "message": "CORS debug information",
        "origin_header": request_origin,
        "allowed_origins": cors_origins,
        "is_allowed": request_origin in cors_origins,
        "request_headers": dict(request.headers),
        "environment": {
            "CORS_ORIGINS": os.getenv('CORS_ORIGINS', 'Not set')
        }
    }))
    
    # Don't manually add CORS headers here; let Flask-CORS handle it
    return response

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@api.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint for resume analysis"""
    try:
        # Check if the required files are in the request
        if 'resume' not in request.files:
            raise BadRequestError("No resume file uploaded")
        
        resume_file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        logger.info(f"Received analyze request with resume: {resume_file.filename}")
        
        # Validate file
        if resume_file.filename == '':
            raise BadRequestError("No file selected")
        
        # Check if the file is a PDF
        if not resume_file.filename.endswith('.pdf'):
            raise BadRequestError("Only PDF files are supported")
        
        # Extract text from PDF
        try:
            resume_text = extract_text_from_pdf(resume_file)
            logger.info("Successfully extracted text from PDF")
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise BadRequestError(f"PDF extraction error: {str(e)}")
        
        # Analyze the resume with Gemini
        try:
            logger.info("Sending resume to Gemini API for analysis")
            gemini_response = analyze_resume_with_gemini(resume_text, job_description)
            
            logger.info("Parsing Gemini response")
            analysis_result = parse_gemini_response(gemini_response)
            
            # Add status key to the response
            if isinstance(analysis_result, dict):
                analysis_result["status"] = "success"
                
                # Log basic info about the result
                logger.info(f"Analysis complete - Score: {analysis_result.get('score', 'N/A')}")
                return jsonify(analysis_result)
            else:
                logger.error("Invalid response format from analysis")
                raise ServerError("Invalid response format from analysis")
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise ServerError(f"Analysis error: {str(e)}")
            
    except BadRequestError as e:
        return jsonify(e.to_dict()), e.status_code
    except ServerError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        error = ServerError(f"Unexpected error: {str(e)}")
        return jsonify(error.to_dict()), error.status_code

@api.route('/analyze-overall', methods=['POST'])
def analyze_overall():
    """API endpoint for overall resume analysis without job description"""
    try:
        # Check if the required files are in the request
        if 'resume' not in request.files:
            raise BadRequestError("No resume file uploaded")
        
        resume_file = request.files['resume']
        
        logger.info(f"Received analyze-overall request with resume: {resume_file.filename}")
        
        # Validate file
        if resume_file.filename == '':
            raise BadRequestError("No file selected")
        
        # Check if the file is a PDF
        if not resume_file.filename.endswith('.pdf'):
            raise BadRequestError("Only PDF files are supported")
        
        # Extract text from PDF
        try:
            resume_text = extract_text_from_pdf(resume_file)
            logger.info("Successfully extracted text from PDF")
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise BadRequestError(f"PDF extraction error: {str(e)}")
        
        # Analyze the resume overall with Gemini
        try:
            logger.info("Sending resume to Gemini API for overall analysis")
            gemini_response = analyze_resume_overall_with_gemini(resume_text)
            
            logger.info("Parsing Gemini response")
            analysis_result = parse_gemini_response(gemini_response)
            
            # Add status key to the response
            if isinstance(analysis_result, dict):
                analysis_result["status"] = "success"
                
                # Log basic info about the result
                logger.info(f"Overall analysis complete - Score: {analysis_result.get('overall_score', 'N/A')}")
                return jsonify(analysis_result)
            else:
                logger.error("Invalid response format from overall analysis")
                raise ServerError("Invalid response format from overall analysis")
        except Exception as e:
            logger.error(f"Overall analysis error: {str(e)}")
            raise ServerError(f"Overall analysis error: {str(e)}")
            
    except BadRequestError as e:
        return jsonify(e.to_dict()), e.status_code
    except ServerError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in analyze-overall: {str(e)}")
        error = ServerError(f"Unexpected error: {str(e)}")
        return jsonify(error.to_dict()), error.status_code
        
@api.route('/test-format', methods=['GET'])
def test_format():
    """Test endpoint that returns a sample analysis result with the expected format"""
    sample_data = {
        "status": "success",
        "score": 75,
        "summary_insights": {
            "overall_grade": "B",
            "ats_readiness": 85,
            "competitiveness": 70,
            "top_strengths": ["Strong technical skills", "Relevant experience", "Good education background"],
            "priority_actions": [
                {
                    "priority": "High",
                    "area": "Skills",
                    "recommendation": "Add missing technical skills like Docker, Kubernetes"
                },
                {
                    "priority": "Medium",
                    "area": "Experience",
                    "recommendation": "Quantify achievements with metrics and results"
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
            "strengths": ["Strong technical background", "Good education credentials"],
            "weaknesses": ["Lack of quantified achievements", "Missing some key skills"],
            "improvement_suggestions": ["Add metrics to achievements", "Include more industry keywords"]
        },
        "ats_analysis": {
            "score": 75,
            "format_issues": ["Complex formatting", "Non-standard headings"],
            "keyword_match": {
                "percentage": 65,
                "matches": ["Python", "JavaScript", "React"],
                "missing": ["Docker", "Kubernetes", "AWS"]
            },
            "recommendations": ["Simplify formatting", "Use standard section headings"]
        },
        "skills_analysis": {
            "matching_skills": ["Python", "JavaScript", "React"],
            "missing_skills": ["Docker", "Kubernetes", "AWS"],
            "additional_skills": ["Vue.js", "GraphQL"]
        },
        "section_feedback": {
            "contact_information": "Contact information is complete and well-formatted.",
            "professional_summary": "Summary could be more targeted to the specific job role.",
            "work_experience": "Good experience but lacks quantified achievements.",
            "education": "Education section is well-formatted and relevant.",
            "skills": "Skills section needs more organization and alignment with job.",
            "projects": "Projects demonstrate relevant experience but need more detail.",
            "certifications": "Certifications are relevant but could be more current."
        },
        "industry_insights": {
            "industry_trends": ["Cloud-native development", "DevOps integration"],
            "recommendations": ["Highlight cloud experience", "Emphasize collaboration skills"]
        },
        "gap_analysis": {
            "identified_gaps": ["Cloud infrastructure experience", "DevOps tooling"],
            "learning_paths": [
                {
                    "gap": "Cloud infrastructure",
                    "recommendations": ["AWS Certified Solutions Architect", "GCP Professional Cloud Architect"]
                },
                {
                    "gap": "DevOps tooling",
                    "recommendations": ["Learn Docker and Kubernetes", "CI/CD pipeline experience"]
                }
            ]
        }
    }
    return jsonify(sample_data)

@api.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and Render's health checks
    Checks API key validity and uploads directory access
    """
    health_status = {
        "status": "ok",
        "message": "Service is running",
        "version": "1.0.0",
        "environment": os.getenv("FLASK_ENV", "development"),
        "checks": {
            "api_key": "ok" if os.getenv("GOOGLE_API_KEY") else "missing",
            "uploads_directory": "ok"
        }
    }
    
    # Check if uploads directory is accessible
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')
    if not os.path.exists(uploads_dir) or not os.access(uploads_dir, os.W_OK):
        health_status["checks"]["uploads_directory"] = "error"
        health_status["status"] = "warning"
    
    return jsonify(health_status)

@api.route('/improve-section', methods=['POST'])
def improve_section():
    """API endpoint for section-wise resume improvement"""
    try:
        # Get request data
        request_data = request.get_json()
        
        if not request_data:
            raise BadRequestError("No JSON data provided")
        
        section_type = request_data.get('section_type', '')
        original_text = request_data.get('original_text', '')
        
        logger.info(f"Received improve-section request for section: {section_type}")
        
        # Validate input
        if not section_type:
            raise BadRequestError("section_type is required")
        
        if not original_text or not original_text.strip():
            raise BadRequestError("original_text is required and cannot be empty")
        
        # Validate section type
        valid_sections = ['summary', 'experience', 'skills', 'education', 'projects']
        if section_type not in valid_sections:
            raise BadRequestError(f"Invalid section_type. Must be one of: {', '.join(valid_sections)}")
        
        # Improve the section with Gemini
        try:
            logger.info("Sending section to Gemini API for improvement")
            gemini_response = improve_resume_section_with_gemini(section_type, original_text)
            
            logger.info("Parsing Gemini improvement response")
            improvement_result = parse_gemini_response(gemini_response)
            
            # Add status key to the response
            if isinstance(improvement_result, dict):
                improvement_result["status"] = "success"
                improvement_result["section_type"] = section_type
                
                # Log basic info about the result
                improvement_score = improvement_result.get('improvement_score', 'N/A')
                logger.info(f"Section improvement complete - Score: {improvement_score}")
                return jsonify(improvement_result)
            else:
                logger.error("Invalid response format from section improvement")
                raise ServerError("Invalid response format from section improvement")
        except Exception as e:
            logger.error(f"Section improvement error: {str(e)}")
            raise ServerError(f"Section improvement error: {str(e)}")
            
    except BadRequestError as e:
        return jsonify(e.to_dict()), e.status_code
    except ServerError as e:
        return jsonify(e.to_dict()), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in improve-section: {str(e)}")
        error = ServerError(f"Unexpected error: {str(e)}")
        return jsonify(error.to_dict()), error.status_code

@api.route('/test-section-improvement', methods=['GET'])
def test_section_improvement():
    """Test endpoint that returns a sample section improvement result"""
    sample_data = {
        "status": "success",
        "section_type": "summary",
        "improved_text": "Results-driven Software Engineer with 5+ years of experience developing scalable web applications using modern frameworks. Proven track record of increasing application performance by 40% and reducing development time by 30% through innovative solutions. Expertise in full-stack development with React, Node.js, and cloud technologies. Strong collaborator with cross-functional teams and passion for delivering high-quality user experiences.",
        "improvement_score": 85,
        "key_improvements": [
            "Added quantified achievements (40% performance increase, 30% time reduction)",
            "Strengthened opening with 'Results-driven' to show impact focus",
            "Included specific technologies and skills relevant to modern development",
            "Enhanced value proposition with concrete examples"
        ],
        "analysis": {
            "original_strengths": [
                "Clear mention of years of experience",
                "Relevant technical skills mentioned",
                "Professional tone"
            ],
            "original_weaknesses": [
                "Lack of quantified achievements",
                "Generic phrasing without specific impact",
                "Missing key technologies and frameworks"
            ],
            "improvements_made": [
                {
                    "category": "Content",
                    "change": "Added specific metrics and quantified results",
                    "reason": "Makes achievements concrete and measurable"
                },
                {
                    "category": "Keywords",
                    "change": "Included modern technologies like React, Node.js, cloud",
                    "reason": "Improves ATS compatibility and shows current skills"
                },
                {
                    "category": "Impact",
                    "change": "Emphasized results and value delivery",
                    "reason": "Shows tangible contributions to employers"
                }
            ]
        },
        "formatting_suggestions": [
            "Keep the summary to 3-4 lines for optimal readability",
            "Use bullet points if the summary becomes longer",
            "Consider bold formatting for key achievements"
        ],
        "ats_optimization": {
            "keyword_density": 75,
            "suggested_keywords": ["full-stack", "scalable", "performance optimization", "cloud technologies"],
            "formatting_score": 80
        },
        "alternatives": [
            {
                "version": "Professional Version",
                "text": "Experienced Software Engineer with 5+ years specializing in full-stack web development. Demonstrated expertise in React, Node.js, and cloud technologies with a proven ability to optimize application performance and streamline development processes. Committed to delivering scalable solutions and exceptional user experiences."
            },
            {
                "version": "Creative Version",
                "text": "Innovative Software Engineer passionate about building next-generation web applications. 5+ years of transforming ideas into high-performance, scalable solutions using cutting-edge technologies. Expert in React and Node.js ecosystem with a track record of boosting team productivity and application efficiency."
            }
        ],
        "tips": [
            "Tailor your summary to each job application by highlighting the most relevant skills",
            "Include 2-3 quantified achievements to demonstrate your impact",
            "Use industry-specific keywords that appear in the job description",
            "Keep it concise but impactful - aim for 3-4 sentences maximum"
        ]
    }
    return jsonify(sample_data)
