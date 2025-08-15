import requests
import json
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def test_section_improvement_api(base_url="http://localhost:5000"):
    """Test the section improvement API endpoint"""
    
    print("\n" + "="*60)
    print("TESTING SECTION IMPROVEMENT API")
    print("="*60)
    
    # Test data
    test_case = {
        "section_type": "summary",
        "original_text": "I am a software developer with 3 years of experience. I know Python and JavaScript and have worked on web applications."
    }
    
    try:
        print(f"Testing: POST {base_url}/improve-section")
        print(f"Section Type: {test_case['section_type']}")
        print(f"Original Text: {test_case['original_text']}")
        print("-" * 40)
        
        response = requests.post(
            f"{base_url}/improve-section",
            json=test_case,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Section improvement successful!")
            print(f"Improvement Score: {result.get('improvement_score', 'N/A')}/100")
            print(f"Number of Key Improvements: {len(result.get('key_improvements', []))}")
            
            # Show improved text
            improved_text = result.get('improved_text', '')
            if improved_text:
                print(f"\nImproved Text:")
                print(f"{improved_text}")
            
            # Show key improvements
            key_improvements = result.get('key_improvements', [])
            if key_improvements:
                print(f"\nKey Improvements Made:")
                for i, improvement in enumerate(key_improvements, 1):
                    print(f"  {i}. {improvement}")
            
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_api_format(pdf_path, job_description=None, base_url="http://localhost:5000"):
    """
    Test the resume analysis API with a PDF file
    
    Args:
        pdf_path (str): Path to the PDF file to analyze
        job_description (str): Job description text or None to use sample
        base_url (str): Base URL of the API
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return
    
    # Use sample job description if none provided
    if not job_description:
        job_description = """
        Software Engineer
        
        Requirements:
        - 3+ years of experience in Python development
        - Strong knowledge of web frameworks like Flask or Django
        - Experience with RESTful APIs
        - Familiarity with frontend technologies (React, Vue)
        - Understanding of database systems
        - Git version control
        
        Responsibilities:
        - Design and develop new features
        - Collaborate with cross-functional teams
        - Write clean, maintainable code
        - Troubleshoot and debug issues
        - Participate in code reviews
        """
    
    print(f"Testing resume analysis API with file: {pdf_path}")
    
    # Prepare the files and data for the request
    files = {'resume': open(pdf_path, 'rb')}
    data = {'job_description': job_description}
    
    try:
        # Test the test-format endpoint first
        print("\nTesting format endpoint...")
        response = requests.get(f"{base_url}/test-format")
        if response.status_code == 200:
            print("Format test endpoint succeeded")
            # Don't print the entire response as it would be too verbose
            print(f"Keys in response: {list(response.json().keys())}")
        else:
            print(f"Format test failed with status code {response.status_code}")
            print(response.text)
        
        # Now test the actual analysis endpoint
        print("\nTesting analysis endpoint with PDF...")
        response = requests.post(f"{base_url}/analyze", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("Analysis succeeded!")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Score: {result.get('score', 'N/A')}")
            
            # Print keys to verify structure
            print("\nResponse structure:")
            print(f"Top-level keys: {list(result.keys())}")
            
            # Save the response to a file for inspection
            with open("api_response.json", "w") as f:
                json.dump(result, f, indent=2)
            
            print("\nResponse saved to api_response.json")
        else:
            print(f"Analysis failed with status code {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        files['resume'].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the resume analysis API")
    parser.add_argument("--pdf", help="Path to the PDF resume file for analysis")
    parser.add_argument("--job", help="Path to a text file containing the job description")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of the API")
    parser.add_argument("--test-section", action="store_true", help="Test section improvement endpoint")
    parser.add_argument("--test-all", action="store_true", help="Test all endpoints")
    
    args = parser.parse_args()
    
    if args.test_all:
        # Test section improvement
        print("Testing all endpoints...")
        test_section_improvement_api(args.url)
        
        # Test analysis if PDF provided
        if args.pdf:
            job_description = None
            if args.job and os.path.exists(args.job):
                with open(args.job, "r") as f:
                    job_description = f.read()
            test_api_format(args.pdf, job_description, args.url)
        else:
            print("\nSkipping resume analysis test (no PDF provided)")
    
    elif args.test_section:
        # Test only section improvement
        test_section_improvement_api(args.url)
    
    elif args.pdf:
        # Test only resume analysis
        job_description = None
        if args.job and os.path.exists(args.job):
            with open(args.job, "r") as f:
                job_description = f.read()
        test_api_format(args.pdf, job_description, args.url)
    
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python test_api.py --test-section                    # Test section improvement only")
        print("  python test_api.py --pdf resume.pdf                  # Test resume analysis only") 
        print("  python test_api.py --test-all --pdf resume.pdf       # Test all endpoints")
        print("  python test_api.py --pdf resume.pdf --job job.txt    # Test with job description")
