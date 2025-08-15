import json
import re

def parse_gemini_response(response_text):
    """
    Parse the response from Gemini API into a structured JSON object
    
    Args:
        response_text (str): The raw text response from Gemini API
        
    Returns:
        dict: A structured JSON object with the analysis results
    """
    try:
        # Clean up the text to handle potential formatting issues
        # Remove markdown code block markers if present
        cleaned_text = re.sub(r'```json|```|\n```', '', response_text)
        
        # Try to parse the response as JSON directly
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the text response
            json_start = cleaned_text.find('{')
            json_end = cleaned_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = cleaned_text[json_start:json_end]
                
                # Remove any comments that might be in the JSON
                json_str = re.sub(r'//.*?(\n|$)', '', json_str)
                
                # Parse the cleaned JSON
                parsed_data = json.loads(json_str)
                
                # Validate and ensure required keys are present
                validate_and_fix_data(parsed_data)
                
                return parsed_data
            else:
                raise Exception("Could not find valid JSON in the response")
    except Exception as e:
        raise Exception(f"Failed to parse model response as JSON: {str(e)}")

def validate_and_fix_data(data):
    """
    Validate and fix the parsed data to ensure all required keys are present
    
    Args:
        data (dict): The parsed data
    """
    # Ensure score is present
    if 'score' not in data:
        data['score'] = 0
    
    # Ensure summary_insights is present
    if 'summary_insights' not in data:
        data['summary_insights'] = {
            'overall_grade': 'N/A',
            'ats_readiness': 0,
            'competitiveness': 0,
            'top_strengths': [],
            'priority_actions': []
        }
    
    # Ensure comprehensive_analysis is present
    if 'comprehensive_analysis' not in data:
        data['comprehensive_analysis'] = {
            'overall_score': data.get('score', 0),
            'detailed_metrics': {},
            'strengths': [],
            'weaknesses': [],
            'improvement_suggestions': []
        }
    
    # Ensure ats_analysis is present
    if 'ats_analysis' not in data:
        data['ats_analysis'] = {
            'score': 0,
            'format_issues': [],
            'keyword_match': {
                'percentage': 0,
                'matches': [],
                'missing': []
            },
            'recommendations': []
        }
    
    # Ensure skills_analysis is present
    if 'skills_analysis' not in data:
        data['skills_analysis'] = {
            'matching_skills': [],
            'missing_skills': [],
            'additional_skills': []
        }
    
    # Ensure section_feedback is present
    if 'section_feedback' not in data:
        data['section_feedback'] = {
            'contact_information': '',
            'professional_summary': '',
            'work_experience': '',
            'education': '',
            'skills': '',
            'projects': '',
            'certifications': ''
        }
    
    # Ensure industry_insights is present
    if 'industry_insights' not in data:
        data['industry_insights'] = {
            'industry_trends': [],
            'recommendations': []
        }
    
    # Ensure gap_analysis is present
    if 'gap_analysis' not in data:
        data['gap_analysis'] = {
            'identified_gaps': [],
            'learning_paths': []
        }
    
    return data
