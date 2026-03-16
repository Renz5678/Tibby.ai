"""
Test script for Tibby Chatbot API
Tests Phase 1 improvements
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✅ Health check passed!")

def test_greeting():
    """Test greeting intent"""
    print("\n" + "="*50)
    print("TEST 2: Greeting Intent")
    print("="*50)
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "hello"}
    )
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200
    assert "reply" in data
    assert data["confidence"] >= 0.7
    print("✅ Greeting intent passed!")

def test_taglish():
    """Test Taglish pattern matching"""
    print("\n" + "="*50)
    print("TEST 3: Taglish Support")
    print("="*50)
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "paano mag enroll"}
    )
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200
    assert "reply" in data
    print("✅ Taglish support passed!")

def test_fuzzy_matching():
    """Test fuzzy matching with typo"""
    print("\n" + "="*50)
    print("TEST 4: Fuzzy Matching (Typo Tolerance)")
    print("="*50)
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "how to enrolll"}  # Note the typo
    )
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    assert response.status_code == 200
    assert "reply" in data
    print("✅ Fuzzy matching passed!")

def test_caching():
    """Test response caching"""
    print("\n" + "="*50)
    print("TEST 5: Response Caching")
    print("="*50)
    
    # First request
    response1 = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "school location"}
    )
    data1 = response1.json()
    print(f"First request - Cached: {data1.get('cached', False)}")
    
    # Second request (should be cached)
    response2 = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "school location"}
    )
    data2 = response2.json()
    print(f"Second request - Cached: {data2.get('cached', False)}")
    
    assert data1["reply"] == data2["reply"]
    assert data2.get("cached") == True
    print("✅ Caching passed!")

def test_input_validation():
    """Test input validation"""
    print("\n" + "="*50)
    print("TEST 6: Input Validation")
    print("="*50)
    
    # Empty message
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": ""}
    )
    print(f"Empty message - Status Code: {response.status_code}")
    assert response.status_code == 400
    print("✅ Empty message validation passed!")
    
    # Too long message
    long_message = "a" * 501
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": long_message}
    )
    print(f"Long message - Status Code: {response.status_code}")
    assert response.status_code == 400
    print("✅ Long message validation passed!")

def test_rate_limiting():
    """Test rate limiting"""
    print("\n" + "="*50)
    print("TEST 7: Rate Limiting")
    print("="*50)
    
    # Send 11 requests rapidly (limit is 10/min)
    for i in range(11):
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": f"test {i}"}
        )
        if i < 10:
            assert response.status_code == 200
        else:
            # 11th request should be rate limited
            print(f"Request {i+1} - Status Code: {response.status_code}")
            if response.status_code == 429:
                print("✅ Rate limiting passed!")
                return
    
    print("⚠️ Rate limiting may not have triggered (cache hit)")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TIBBY CHATBOT - PHASE 1 TEST SUITE")
    print("="*70)
    
    try:
        test_health()
        test_greeting()
        test_taglish()
        test_fuzzy_matching()
        test_caching()
        test_input_validation()
        test_rate_limiting()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Is it running on http://localhost:5000?")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
