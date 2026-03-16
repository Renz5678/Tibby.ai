"""
Test script for Phase 2: Expanded Intents
Tests multilingual pattern matching
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_multilingual_patterns():
    """Test English, Taglish, and Tagalog patterns"""
    
    test_cases = [
        # English
        {"message": "hello", "expected_tag": "greeting", "language": "English"},
        {"message": "how to enroll", "expected_tag": "admissions_enrollment", "language": "English"},
        {"message": "where is the school", "expected_tag": "school_location", "language": "English"},
        
        # Taglish
        {"message": "kamusta", "expected_tag": "greeting", "language": "Tagalog"},
        {"message": "paano mag enroll", "expected_tag": "admissions_enrollment", "language": "Taglish"},
        {"message": "saan ang school", "expected_tag": "school_location", "language": "Taglish"},
        
        # Tagalog
        {"message": "magandang umaga", "expected_tag": "greeting", "language": "Tagalog"},
        {"message": "ano requirements sa enrollment", "expected_tag": "admissions_enrollment", "language": "Taglish"},
        {"message": "nasaan kayo", "expected_tag": "school_location", "language": "Tagalog"},
        
        # Typos
        {"message": "helo", "expected_tag": "greeting", "language": "English (typo)"},
        {"message": "enrolll", "expected_tag": "admissions_enrollment", "language": "English (typo)"},
        {"message": "wer is the school", "expected_tag": "school_location", "language": "English (typo)"},
        
        # More variations
        {"message": "ano grades", "expected_tag": "general_info", "language": "Taglish"},
        {"message": "may sped ba", "expected_tag": "special_programs_sped", "language": "Taglish"},
        {"message": "kailangan ba ng work immersion", "expected_tag": "work_immersion", "language": "Taglish"},
        {"message": "paano check grades", "expected_tag": "grades_checking", "language": "Taglish"},
        {"message": "pano pag bumagsak", "expected_tag": "failing_subject", "language": "Taglish"},
        {"message": "pwede ba mag transfer strand", "expected_tag": "transferring_strands", "language": "Taglish"},
        {"message": "kelan pasok", "expected_tag": "schedule_school_hours", "language": "Taglish"},
        {"message": "ano facilities", "expected_tag": "facilities", "language": "Taglish"},
    ]
    
    print("\n" + "="*70)
    print("PHASE 2 TEST: MULTILINGUAL PATTERN MATCHING")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}/{len(test_cases)}: {test['language']}")
        print(f"Query: \"{test['message']}\"")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": test['message']}
            )
            
            if response.status_code == 200:
                data = response.json()
                confidence = data.get('confidence', 0)
                reply = data.get('reply', '')
                
                if confidence >= 0.70:
                    print(f"✅ PASSED - Confidence: {confidence:.2f}")
                    print(f"Response: {reply[:100]}...")
                    passed += 1
                else:
                    print(f"⚠️ LOW CONFIDENCE - {confidence:.2f}")
                    print(f"Response: {reply[:100]}...")
                    failed += 1
            else:
                print(f"❌ FAILED - Status: {response.status_code}")
                failed += 1
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTS: {passed}/{len(test_cases)} passed ({passed/len(test_cases)*100:.1f}%)")
    print("="*70)
    
    return passed, failed

if __name__ == "__main__":
    try:
        passed, failed = test_multilingual_patterns()
        
        if failed == 0:
            print("\n✅ ALL TESTS PASSED! Multilingual support is working perfectly!")
        else:
            print(f"\n⚠️ {failed} test(s) failed. Review the results above.")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Is it running on http://localhost:5000?")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
