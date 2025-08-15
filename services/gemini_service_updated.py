import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file if present
load_dotenv()

# Configure environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY not set. Gemini API calls will fail.")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
model = genai.GenerativeModel('gemini-2.5-flash')

def analyze_resume_with_gemini(resume_text, job_description):
    """
    Send resume text and job description to Gemini API for analysis
    
    Args:
        resume_text (str): The extracted text from the resume PDF
        job_description (str): The job description provided by the user
        
    Returns:
        dict: The analysis results structured as a JSON object
    """
    
    # Prepare the prompt for Gemini
    prompt = f"""
    You are an expert resume analyst and career advisor. Analyze the following resume against the provided job description.
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Provide a comprehensive analysis as a JSON object with EXACTLY the following structure:

    {{
      "score": 75, // Overall job match score from 0-100
      
      "summary_insights": {{
        "overall_grade": "B", // Single letter grade (A, B, C, D, F)
        "ats_readiness": 85, // Score from 0-100
        "competitiveness": 70, // Score from 0-100 for market competitiveness
        "experience_level": {{
          "resume_level": "Mid-level", // Junior, Mid-level, Senior
          "job_level": "Mid-level", // Junior, Mid-level, Senior
          "match": true, // Boolean indicating if levels match
          "mismatch_details": "The experience levels align well." // Only provided when there's a mismatch
        }},
        "top_strengths": ["Strength 1", "Strength 2", "Strength 3"], // 3-5 key strengths
        "priority_actions": [
          {{
            "priority": "High", // High, Medium, Low
            "area": "Skills", // Area to improve
            "recommendation": "Add missing technical skills like X, Y, Z"
          }}
          // 2-4 priority actions
        ]
      }},
      
      "comprehensive_analysis": {{
        "overall_score": 75, // Same as score above
        "detailed_metrics": {{
          "relevance": {{
            "score": 80,
            "details": {{
              "experience_match": 85,
              "education_match": 75
            }}
          }},
          "ats_compatibility": {{
            "score": 70,
            "details": {{
              "keyword_density": 65, 
              "format_score": 75
            }}
          }},
          "content_quality": {{
            "score": 75,
            "details": {{
              "clarity": 70,
              "impact": 80
            }}
          }},
          "skills_alignment": {{
            "score": 65,
            "details": {{
              "matching_skills_percentage": 65,
              "missing_critical_skills": 4
            }}
          }}
        }},
        "strengths": ["Detailed strength 1", "Detailed strength 2"],
        "weaknesses": ["Detailed weakness 1", "Detailed weakness 2"],
        "improvement_suggestions": ["Improvement suggestion 1", "Improvement suggestion 2"]
      }},
      
      "ats_analysis": {{
        "score": 75, // ATS score from 0-100
        "format_issues": ["Issue 1", "Issue 2"], // List any formatting issues
        "keyword_match": {{
          "percentage": 65, // Overall keyword match percentage
          "matches": ["Keyword 1", "Keyword 2"], // Keywords found in both
          "missing": ["Missing keyword 1", "Missing keyword 2"] // Important keywords missing
        }},
        "recommendations": ["ATS recommendation 1", "ATS recommendation 2"]
      }},
      
      "skills_analysis": {{
        "matching_skills": ["Skill 1", "Skill 2"], // Skills found in both resume and job
        "missing_skills": ["Missing skill 1", "Missing skill 2"], // Skills in job but not resume
        "additional_skills": ["Additional skill 1"] // Skills in resume but not job
      }},
      
      "section_feedback": {{
        "contact_information": "Feedback on contact section...",
        "professional_summary": "Feedback on summary...",
        "work_experience": "Feedback on work experience...",
        "education": "Feedback on education...",
        "skills": "Feedback on skills section...",
        "projects": "Feedback on projects...",
        "certifications": "Feedback on certifications..."
      }},
      
      "industry_insights": {{
        "industry_trends": ["Trend 1", "Trend 2"],
        "recommendations": ["Industry recommendation 1", "Industry recommendation 2"]
      }},
      
      "gap_analysis": {{
        "identified_gaps": ["Gap 1", "Gap 2"],
        "learning_paths": [
          {{
            "gap": "Gap 1",
            "recommendations": ["Learning recommendation 1", "Learning recommendation 2"]
          }}
        ]
      }}
    }}

    Ensure ALL keys are present even if values are empty arrays or default values. DO NOT include any explanation or text outside the JSON structure.
    """
    
    try:
        # Generate response from Gemini
        response = model.generate_content(prompt)
        
        # Return the response text - will be parsed by the parser
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise Exception(f"Error analyzing resume: {str(e)}")


def analyze_resume_overall_with_gemini(resume_text):
    """
    Send resume text to Gemini API for overall analysis without job description
    
    Args:
        resume_text (str): The extracted text from the resume PDF
        
    Returns:
        dict: The analysis results structured as a JSON object
    """
    
    # Prepare the prompt for Gemini
    prompt = f"""
    You are an expert resume analyst and career advisor. Analyze the following resume to provide comprehensive overall insights about its quality, effectiveness, and areas for improvement.
    
    RESUME:
    {resume_text}
    
    Provide a comprehensive overall analysis as a JSON object with EXACTLY the following structure:

    {{
      "overall_score": 75, // Overall resume quality score from 0-100
      
      "summary_insights": {{
        "overall_grade": "B", // Single letter grade (A, B, C, D, F)
        "ats_readiness": 85, // Score from 0-100 for ATS compatibility
        "market_competitiveness": 70, // Score from 0-100 for market competitiveness
        "professional_presentation": 80, // Score from 0-100 for overall presentation
        "experience_level": "Mid-level", // Junior, Mid-level, or Senior classification
        "top_strengths": ["Strong technical skills", "Relevant experience", "Good education background"], // 3-5 key strengths
        "priority_improvements": [
          {{
            "priority": "High", // High, Medium, Low
            "area": "Skills", // Area to improve
            "recommendation": "Organize skills section and add trending technologies"
          }}
          // 2-4 priority improvement areas
        ]
      }},
      
      "detailed_analysis": {{
        "content_quality": {{
          "score": 75,
          "details": {{
            "clarity_and_impact": 70,
            "achievement_quantification": 65,
            "keyword_optimization": 80,
            "professional_language": 85
          }}
        }},
        "structure_and_format": {{
          "score": 80,
          "details": {{
            "organization": 85,
            "readability": 75,
            "consistency": 80,
            "visual_appeal": 70
          }}
        }},
        "ats_compatibility": {{
          "score": 70,
          "details": {{
            "format_compatibility": 75, 
            "keyword_density": 65,
            "section_headers": 80,
            "file_structure": 70
          }}
        }},
        "completeness": {{
          "score": 85,
          "details": {{
            "essential_sections": 90,
            "contact_information": 95,
            "work_history": 80,
            "skills_coverage": 75
          }}
        }}
      }},
      
      "section_analysis": {{
        "contact_information": {{
          "score": 95,
          "feedback": "Contact information is complete and professional",
          "suggestions": ["Consider adding LinkedIn profile", "Ensure phone number is formatted consistently"]
        }},
        "professional_summary": {{
          "score": 75,
          "feedback": "Summary provides good overview but could be more impactful",
          "suggestions": ["Add quantified achievements", "Make it more targeted and compelling"]
        }},
        "work_experience": {{
          "score": 70,
          "feedback": "Experience shows progression but lacks quantified achievements",
          "suggestions": ["Add metrics and numbers", "Use stronger action verbs", "Focus on achievements vs responsibilities"]
        }},
        "education": {{
          "score": 85,
          "feedback": "Education section is well-formatted and relevant",
          "suggestions": ["Consider adding relevant coursework", "Include GPA if strong"]
        }},
        "skills": {{
          "score": 65,
          "feedback": "Skills section needs better organization and more current technologies",
          "suggestions": ["Organize by category", "Add trending technologies", "Remove outdated skills"]
        }},
        "projects": {{
          "score": 70,
          "feedback": "Projects demonstrate skills but need more detail",
          "suggestions": ["Add more technical details", "Include project outcomes", "Highlight technologies used"]
        }},
        "certifications": {{
          "score": 80,
          "feedback": "Certifications are relevant and current",
          "suggestions": ["Add expiration dates", "Include certification numbers"]
        }}
      }},
      
      "strengths": [
        "Clear professional progression in experience",
        "Strong educational background",
        "Good mix of technical and soft skills",
        "Professional formatting and layout"
      ],
      
      "improvement_areas": [
        "Lack of quantified achievements and metrics",
        "Skills section organization could be improved", 
        "Missing some trending industry technologies",
        "Could benefit from more impactful summary"
      ],
      
      "ats_analysis": {{
        "score": 75,
        "strengths": ["Standard section headers", "Good keyword usage", "Clean formatting"],
        "issues": ["Some complex formatting", "Missing key industry terms"],
        "recommendations": [
          "Use more standard fonts and formatting",
          "Add more industry-specific keywords",
          "Ensure consistent heading styles"
        ]
      }},
      
      "industry_insights": {{
        "current_trends": ["Cloud computing adoption", "AI/ML integration", "Remote work capabilities"],
        "skill_recommendations": ["Cloud platforms (AWS, Azure)", "DevOps tools", "Modern frameworks"],
        "market_positioning": "Candidate shows solid foundation but needs to modernize skills portfolio"
      }},
      
      "actionable_recommendations": [
        {{
          "category": "Content",
          "priority": "High",
          "action": "Add quantified achievements to work experience",
          "impact": "Significantly improves credibility and demonstrates value"
        }},
        {{
          "category": "Skills",
          "priority": "High", 
          "action": "Reorganize skills section and add trending technologies",
          "impact": "Better ATS compatibility and shows current market relevance"
        }},
        {{
          "category": "Format",
          "priority": "Medium",
          "action": "Ensure consistent formatting throughout",
          "impact": "Improves professional appearance and readability"
        }}
      ]
    }}

    Guidelines for analysis:
    1. Focus on overall resume quality and effectiveness
    2. Evaluate ATS compatibility and modern hiring practices
    3. Assess market competitiveness in current job market
    4. Provide specific, actionable feedback
    5. Consider industry standards and best practices
    6. Evaluate both content and presentation
    7. Identify gaps in skills or experience presentation
    8. Classify the resume's experience level as Junior, Mid-level, or Senior

    Ensure ALL keys are present even if values are empty arrays or default values. DO NOT include any explanation or text outside the JSON structure.
    """
    
    try:
        # Generate response from Gemini
        response = model.generate_content(prompt)
        
        # Return the response text - will be parsed by the parser
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API for overall analysis: {e}")
        raise Exception(f"Error analyzing resume overall: {str(e)}")


def improve_resume_section_with_gemini(section_type, original_text):
    """
    Send section text to Gemini API for improvement suggestions
    
    Args:
        section_type (str): The type of section (summary, experience, skills, education, projects)
        original_text (str): The original text of the section to improve
        
    Returns:
        dict: The improvement suggestions structured as a JSON object
    """
    
    # Define section-specific improvement prompts
    section_prompts = {
        "summary": {
            "title": "Professional Summary",
            "context": "This is a professional summary/objective section that should be compelling, concise, and tailored to showcase the candidate's value proposition.",
            "focus": "Make it more impactful, quantify achievements, highlight key strengths, and ensure it's ATS-friendly."
        },
        "experience": {
            "title": "Work Experience",
            "context": "This is a work experience section that should showcase achievements, responsibilities, and impact in previous roles.",
            "focus": "Use action verbs, quantify achievements with metrics, show progression, and highlight relevant accomplishments."
        },
        "skills": {
            "title": "Skills Section",
            "context": "This is a skills section that should list technical and soft skills relevant to the target role.",
            "focus": "Organize skills by category, prioritize relevant skills, include trending technologies, and ensure keyword optimization."
        },
        "education": {
            "title": "Education",
            "context": "This is an education section that should highlight academic achievements, relevant coursework, and certifications.",
            "focus": "Highlight relevant coursework, academic achievements, certifications, and any honors or distinctions."
        },
        "projects": {
            "title": "Projects",
            "context": "This is a projects section that should showcase personal or professional projects demonstrating skills and experience.",
            "focus": "Highlight technologies used, quantify impact, show problem-solving abilities, and demonstrate relevant skills."
        }
    }
    
    section_info = section_prompts.get(section_type, section_prompts["summary"])
    
    # Prepare the prompt for Gemini
    prompt = f"""
    You are an expert resume writer and career coach. I need you to improve a {section_info['title']} section of a resume.

    SECTION TYPE: {section_info['title']}
    CONTEXT: {section_info['context']}
    IMPROVEMENT FOCUS: {section_info['focus']}

    ORIGINAL TEXT:
    {original_text}

    Please provide comprehensive improvement suggestions as a JSON object with EXACTLY the following structure:

    {{
      "improved_text": "The completely rewritten and improved version of the section text",
      "improvement_score": 85, // Score from 0-100 indicating how much improvement was made
      "key_improvements": [
        "Specific improvement 1 made to the text",
        "Specific improvement 2 made to the text",
        "Specific improvement 3 made to the text"
      ],
      "analysis": {{
        "original_strengths": ["Strength 1 of original text", "Strength 2"],
        "original_weaknesses": ["Weakness 1 of original text", "Weakness 2"],
        "improvements_made": [
          {{
            "category": "Content", // Content, Structure, Keywords, Impact, etc.
            "change": "Description of what was changed",
            "reason": "Why this change improves the section"
          }},
          {{
            "category": "Keywords",
            "change": "Added industry-relevant keywords",
            "reason": "Improves ATS compatibility and relevance"
          }}
        ]
      }},
      "formatting_suggestions": [
        "Formatting suggestion 1",
        "Formatting suggestion 2"
      ],
      "ats_optimization": {{
        "keyword_density": 75, // Score from 0-100
        "suggested_keywords": ["keyword1", "keyword2", "keyword3"],
        "formatting_score": 80 // Score from 0-100
      }},
      "alternatives": [
        {{
          "version": "Professional Version",
          "text": "Alternative version 1 of the improved text"
        }},
        {{
          "version": "Creative Version", 
          "text": "Alternative version 2 of the improved text"
        }}
      ],
      "tips": [
        "Additional tip 1 for this section type",
        "Additional tip 2 for this section type"
      ]
    }}

    Guidelines for improvement:
    1. Make the text more impactful and results-oriented
    2. Use strong action verbs and quantify achievements where possible
    3. Optimize for ATS (Applicant Tracking Systems) with relevant keywords
    4. Ensure the tone is professional and appropriate
    5. Make it concise but comprehensive
    6. Focus on value proposition and unique selling points
    7. Use industry-standard terminology and best practices

    Ensure ALL keys are present even if values are empty arrays or default values. DO NOT include any explanation or text outside the JSON structure.
    """
    
    try:
        # Generate response from Gemini
        response = model.generate_content(prompt)
        
        # Return the response text - will be parsed by the parser
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API for section improvement: {e}")
        raise Exception(f"Error improving section: {str(e)}")
