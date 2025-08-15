rimport requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_section_improvement():
    """Test the section improvement endpoint"""
    
    # Test data for different section types
    test_cases = [
        {
            "section_type": "summary",
            "original_text": "I am a software developer with experience in programming. I know JavaScript and Python and have worked on some projects."
        },
        {
            "section_type": "experience", 
            "original_text": "Software Developer at TechCorp\n• Worked on web applications\n• Used React and Node.js\n• Collaborated with team members"
        },
        {
            "section_type": "skills",
            "original_text": "Programming Languages: JavaScript, Python\nFrameworks: React\nOther: Git, HTML, CSS"
        }
    ]
    
    print("Testing Section Improvement API...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['section_type'].title()} Section")
        print("-" * 30)
        
        try:
            # Make API request
            response = requests.post(
                f"{BASE_URL}/improve-section",
                json=test_case,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Improvement Score: {result.get('improvement_score', 'N/A')}")
                print(f"Key Improvements: {len(result.get('key_improvements', []))}")
                print(f"Improved Text Preview: {result.get('improved_text', '')[:100]}...")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")

def test_invalid_requests():
    """Test the API with invalid requests"""
    
    print("\n\nTesting Invalid Requests...")
    print("=" * 50)
    
    invalid_cases = [
        {
            "name": "Missing section_type",
            "data": {"original_text": "Some text"}
        },
        {
            "name": "Missing original_text", 
            "data": {"section_type": "summary"}
        },
        {
            "name": "Invalid section_type",
            "data": {
                "section_type": "invalid_section",
                "original_text": "Some text"
            }
        },
        {
            "name": "Empty original_text",
            "data": {
                "section_type": "summary",
                "original_text": ""
            }
        }
    ]
    
    for test_case in invalid_cases:
        print(f"\nTesting: {test_case['name']}")
        print("-" * 20)
        
        try:
            response = requests.post(
                f"{BASE_URL}/improve-section",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 400:
                print("✅ Correctly returned 400 error")
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'No error message')}")
            else:
                print(f"❌ Unexpected status code: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")

def test_sample_endpoint():
    """Test the sample endpoint"""
    
    print("\n\nTesting Sample Endpoint...")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/test-section-improvement")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Sample endpoint working!")
            print(f"Sample data structure keys: {list(result.keys())}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")

if __name__ == "__main__":
    # Test the sample endpoint first
    test_sample_endpoint()
    
    # Test invalid requests
    test_invalid_requests()
    
    # Test actual section improvement (requires Gemini API key)
    print("\n" + "=" * 60)
    print("NOTE: The following tests require a valid GOOGLE_API_KEY")
    print("If you see connection errors, make sure the Flask server is running")
    print("=" * 60)
    
    test_section_improvement()
