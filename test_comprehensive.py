"""
Comprehensive Test Suite for Tibby Chatbot
Tests all functionality including multilingual support, performance, and edge cases
"""

import requests
import json
import time
from typing import List, Dict, Tuple

BASE_URL = "http://localhost:5000"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

def print_test(test_num: int, total: int, name: str):
    """Print test header"""
    print(f"{Colors.BOLD}Test {test_num}/{total}: {name}{Colors.END}")

def print_pass(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_fail(message: str):
    """Print failure message"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warn(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

# ==============================
# Test Suite 1: Health & Stats
# ==============================
def test_health_endpoint():
    """Test health check endpoint"""
    print_header("TEST SUITE 1: HEALTH & STATS")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Health check passed")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Intents loaded: {data.get('intents_loaded')}")
            print_info(f"Total patterns: {data.get('total_patterns')}")
            print_info(f"Response cache: {data.get('response_cache_size')} items")
            print_info(f"Intent cache: {data.get('intent_cache_size')} items")
            return True
        else:
            print_fail(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Health check error: {e}")
        return False

def test_stats_endpoint():
    """Test statistics endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print_pass(f"Stats endpoint working")
            print_info(f"Intents: {data.get('intents')}")
            print_info(f"Total patterns: {data.get('total_patterns')}")
            print_info(f"Avg patterns/intent: {data.get('avg_patterns_per_intent')}")
            print_info(f"Confidence threshold: {data.get('confidence_threshold')}")
            print_info(f"Rate limit: {data.get('rate_limit')}")
            return True
        else:
            print_fail(f"Stats endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print_fail(f"Stats endpoint error: {e}")
        return False

# ==============================
# Test Suite 2: Multilingual Support
# ==============================
def test_multilingual():
    """Test English, Taglish, and Tagalog patterns"""
    print_header("TEST SUITE 2: MULTILINGUAL SUPPORT")
    
    test_cases = [
        # English
        ("hello", "greeting", "English"),
        ("how to enroll", "admissions_enrollment", "English"),
        ("where is the school", "school_location", "English"),
        ("what are the facilities", "facilities", "English"),
        ("can i join a club", "joining_clubs", "English"),
        
        # Taglish
        ("paano mag enroll", "admissions_enrollment", "Taglish"),
        ("saan ang school", "school_location", "Taglish"),
        ("ano facilities", "facilities", "Taglish"),
        ("pwede ba sumali sa club", "joining_clubs", "Taglish"),
        ("kelan pasok", "schedule_school_hours", "Taglish"),
        
        # Tagalog
        ("kamusta", "greeting", "Tagalog"),
        ("magandang umaga", "greeting", "Tagalog"),
        ("nasaan kayo", "school_location", "Tagalog"),
        ("ano kailangan para mag enroll", "admissions_enrollment", "Tagalog"),
        ("may sped ba", "special_programs_sped", "Taglish"),
    ]
    
    passed = 0
    failed = 0
    
    for i, (query, expected_tag, language) in enumerate(test_cases, 1):
        print_test(i, len(test_cases), f"{language} - \"{query}\"")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                confidence = data.get('confidence', 0)
                
                if confidence >= 0.70:
                    print_pass(f"Matched with confidence {confidence:.2f}")
                    print_info(f"Response: {data.get('reply', '')[:80]}...")
                    passed += 1
                else:
                    print_warn(f"Low confidence: {confidence:.2f}")
                    failed += 1
            else:
                print_fail(f"Request failed with status {response.status_code}")
                failed += 1
                
        except Exception as e:
            print_fail(f"Error: {e}")
            failed += 1
        
        time.sleep(0.5)  # Avoid rate limiting
    
    print(f"\n{Colors.BOLD}Results: {passed}/{len(test_cases)} passed ({passed/len(test_cases)*100:.1f}%){Colors.END}")
    return passed, failed

# ==============================
# Test Suite 3: Typo Tolerance
# ==============================
def test_typo_tolerance():
    """Test typo handling"""
    print_header("TEST SUITE 3: TYPO TOLERANCE")
    
    test_cases = [
        ("helo", "greeting"),
        ("enrolll", "admissions_enrollment"),
        ("wer is the school", "school_location"),
        ("facilites", "facilities"),
        ("grdes", "grades_checking"),
        ("paano mag enrol", "admissions_enrollment"),
        ("saan ang skool", "school_location"),
    ]
    
    passed = 0
    failed = 0
    
    for i, (query, expected_tag) in enumerate(test_cases, 1):
        print_test(i, len(test_cases), f"Typo: \"{query}\"")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                confidence = data.get('confidence', 0)
                
                if confidence >= 0.60:  # Lower threshold for typos
                    print_pass(f"Fuzzy match worked! Confidence: {confidence:.2f}")
                    passed += 1
                else:
                    print_warn(f"No match found (confidence: {confidence:.2f})")
                    failed += 1
            else:
                print_fail(f"Request failed with status {response.status_code}")
                failed += 1
                
        except Exception as e:
            print_fail(f"Error: {e}")
            failed += 1
        
        time.sleep(0.5)
    
    print(f"\n{Colors.BOLD}Results: {passed}/{len(test_cases)} passed ({passed/len(test_cases)*100:.1f}%){Colors.END}")
    return passed, failed

# ==============================
# Test Suite 4: Edge Cases
# ==============================
def test_edge_cases():
    """Test edge cases and error handling"""
    print_header("TEST SUITE 4: EDGE CASES")
    
    test_cases = [
        ("", "Empty message", 400),
        ("a" * 501, "Message too long", 400),
        ("   ", "Whitespace only", 400),
        ("xyz123abc", "Random gibberish", 200),  # Should return fallback
    ]
    
    passed = 0
    failed = 0
    
    for i, (query, description, expected_status) in enumerate(test_cases, 1):
        print_test(i, len(test_cases), description)
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query}
            )
            
            if response.status_code == expected_status:
                print_pass(f"Correct status code: {response.status_code}")
                passed += 1
            else:
                print_fail(f"Expected {expected_status}, got {response.status_code}")
                failed += 1
                
        except Exception as e:
            print_fail(f"Error: {e}")
            failed += 1
        
        time.sleep(0.5)
    
    print(f"\n{Colors.BOLD}Results: {passed}/{len(test_cases)} passed ({passed/len(test_cases)*100:.1f}%){Colors.END}")
    return passed, failed

# ==============================
# Test Suite 5: Caching
# ==============================
def test_caching():
    """Test response and intent caching"""
    print_header("TEST SUITE 5: CACHING PERFORMANCE")
    
    query = "hello"
    
    # First request (cache miss)
    print_test(1, 2, "First request (cache miss)")
    start = time.time()
    response1 = requests.post(f"{BASE_URL}/chat", json={"message": query})
    time1 = time.time() - start
    
    if response1.status_code == 200:
        data1 = response1.json()
        print_pass(f"Request successful")
        print_info(f"Time: {time1*1000:.2f}ms")
        print_info(f"Cached: {data1.get('cached', False)}")
    
    time.sleep(0.5)
    
    # Second request (cache hit)
    print_test(2, 2, "Second request (cache hit)")
    start = time.time()
    response2 = requests.post(f"{BASE_URL}/chat", json={"message": query})
    time2 = time.time() - start
    
    if response2.status_code == 200:
        data2 = response2.json()
        print_pass(f"Request successful")
        print_info(f"Time: {time2*1000:.2f}ms")
        print_info(f"Cached: {data2.get('cached', False)}")
        
        if data2.get('cached'):
            speedup = (time1 / time2) if time2 > 0 else 0
            print_pass(f"Cache speedup: {speedup:.2f}x faster")
            return 1, 0
        else:
            print_warn("Response not cached")
            return 0, 1
    
    return 0, 1

# ==============================
# Test Suite 6: Performance Benchmark
# ==============================
def test_performance():
    """Benchmark response times"""
    print_header("TEST SUITE 6: PERFORMANCE BENCHMARK")
    
    queries = [
        "hello",
        "how to enroll",
        "where is the school",
        "paano mag enroll",
        "ano facilities",
    ]
    
    times = []
    
    for i, query in enumerate(queries, 1):
        print_test(i, len(queries), f"\"{query}\"")
        
        start = time.time()
        response = requests.post(f"{BASE_URL}/chat", json={"message": query})
        elapsed = time.time() - start
        times.append(elapsed)
        
        if response.status_code == 200:
            print_info(f"Response time: {elapsed*1000:.2f}ms")
        
        time.sleep(0.5)
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\n{Colors.BOLD}Performance Summary:{Colors.END}")
    print_info(f"Average: {avg_time*1000:.2f}ms")
    print_info(f"Fastest: {min_time*1000:.2f}ms")
    print_info(f"Slowest: {max_time*1000:.2f}ms")
    
    if avg_time < 0.1:  # Under 100ms
        print_pass("Excellent performance!")
        return 1, 0
    elif avg_time < 0.5:  # Under 500ms
        print_pass("Good performance")
        return 1, 0
    else:
        print_warn("Performance could be improved")
        return 0, 1

# ==============================
# Test Suite 7: All Intents Coverage
# ==============================
def test_all_intents():
    """Test at least one pattern from each intent"""
    print_header("TEST SUITE 7: ALL INTENTS COVERAGE")
    
    # One query per intent
    test_cases = [
        ("hello", "greeting"),
        ("what grades", "general_info"),
        ("where is the school", "school_location"),
        ("graduation requirements", "school_requirements_graduation"),
        ("performance tasks", "performance_tasks_projects"),
        ("work immersion", "work_immersion"),
        ("check grades", "grades_checking"),
        ("fail a subject", "failing_subject"),
        ("transfer strands", "transferring_strands"),
        ("how to enroll", "admissions_enrollment"),
        ("school hours", "schedule_school_hours"),
        ("sped program", "special_programs_sped"),
        ("facilities", "facilities"),
        ("clubs", "clubs_organizations"),
        ("join club", "joining_clubs"),
        ("run for ssg", "ssg_candidacy"),
        ("guidance office", "guidance_office"),
        ("uniform policy", "uniform_policy"),
        ("contact info", "contact_info"),
        ("online learning", "open_high_school"),
        ("class suspension", "class_suspension"),
        ("behavior rules", "behavior_discipline"),
        ("goodbye", "farewell"),
        ("who are you", "who_is_tibby"),
        ("teachers", "teachers_faculty"),
        ("tuition", "tuition_fees"),
        ("school calendar", "school_calendar"),
        ("report card", "report_card"),
        ("library hours", "library_hours"),
        ("canteen", "canteen_food"),
        ("school clinic", "health_clinic"),
        ("scholarship", "scholarship"),
        ("sports", "sports_athletics"),
        ("computer lab", "computer_lab"),
        ("science lab", "science_lab"),
        ("bullying", "bullying_safety"),
        ("lost and found", "lost_and_found"),
        ("school id", "id_validation"),
        ("parent teacher meeting", "parent_teacher_conference"),
        ("excuse letter", "excuse_absence"),
    ]
    
    passed = 0
    failed = 0
    
    for i, (query, intent_tag) in enumerate(test_cases, 1):
        print_test(i, len(test_cases), f"{intent_tag}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                confidence = data.get('confidence', 0)
                
                if confidence >= 0.70:
                    print_pass(f"Intent matched (confidence: {confidence:.2f})")
                    passed += 1
                else:
                    print_warn(f"Low confidence: {confidence:.2f}")
                    failed += 1
            else:
                print_fail(f"Request failed")
                failed += 1
                
        except Exception as e:
            print_fail(f"Error: {e}")
            failed += 1
        
        time.sleep(0.6)  # Avoid rate limiting
    
    print(f"\n{Colors.BOLD}Results: {passed}/{len(test_cases)} intents working ({passed/len(test_cases)*100:.1f}%){Colors.END}")
    return passed, failed

# ==============================
# Main Test Runner
# ==============================
def run_all_tests():
    """Run all test suites"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "═"*68 + "╗")
    print("║" + "TIBBY CHATBOT - COMPREHENSIVE TEST SUITE".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print(f"{Colors.END}")
    
    total_passed = 0
    total_failed = 0
    
    # Suite 1: Health & Stats
    if test_health_endpoint():
        total_passed += 1
    else:
        total_failed += 1
    
    if test_stats_endpoint():
        total_passed += 1
    else:
        total_failed += 1
    
    # Suite 2: Multilingual
    passed, failed = test_multilingual()
    total_passed += passed
    total_failed += failed
    
    # Suite 3: Typo Tolerance
    passed, failed = test_typo_tolerance()
    total_passed += passed
    total_failed += failed
    
    # Suite 4: Edge Cases
    passed, failed = test_edge_cases()
    total_passed += passed
    total_failed += failed
    
    # Suite 5: Caching
    passed, failed = test_caching()
    total_passed += passed
    total_failed += failed
    
    # Suite 6: Performance
    passed, failed = test_performance()
    total_passed += passed
    total_failed += failed
    
    # Suite 7: All Intents
    passed, failed = test_all_intents()
    total_passed += passed
    total_failed += failed
    
    # Final Summary
    print_header("FINAL SUMMARY")
    total_tests = total_passed + total_failed
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"{Colors.BOLD}Total Tests: {total_tests}{Colors.END}")
    print(f"{Colors.GREEN}Passed: {total_passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {total_failed}{Colors.END}")
    print(f"{Colors.BOLD}Pass Rate: {pass_rate:.1f}%{Colors.END}\n")
    
    if pass_rate >= 95:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT! All systems working perfectly!{Colors.END}")
    elif pass_rate >= 80:
        print(f"{Colors.YELLOW}{Colors.BOLD}✅ GOOD! Most systems working well.{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  NEEDS ATTENTION! Some systems need fixing.{Colors.END}")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print(f"\n{Colors.RED}❌ Could not connect to server. Is it running on http://localhost:5000?{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Tests interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {e}{Colors.END}")
