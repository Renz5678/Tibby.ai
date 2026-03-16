"""
Tibby Chatbot - Flask Application (Improved)
A friendly chatbot for General Tiburcio de Leon National High School (GTDLNHS)
that answers school-related queries using intent matching and Gemini AI fallback.

IMPROVEMENTS:
- Fixed intent matching regex bug
- Added CORS support for React frontend
- Optimized for Gemini free tier
- Better error handling
- Input validation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
import json
import difflib
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import OrderedDict

app = Flask(__name__)

# ==============================
# CORS Configuration
# ==============================
# Build allowed origins list, filtering out empty strings
_allowed_origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative dev port
    "https://tibby-chatbot.vercel.app",  # Production frontend
]
_custom_origin = os.getenv("FRONTEND_URL", "").strip()
if _custom_origin:
    _allowed_origins.append(_custom_origin)

CORS(app, resources={
    r"/*": {
        "origins": _allowed_origins
    }
})

# ==============================
# Configuration
# ==============================
INTENTS_FILE = "intents.json"

# Free tier rate limiting
RATE_LIMIT_REQUESTS = 10  # requests per minute per user
RATE_LIMIT_WINDOW = 60  # seconds

# Cache configuration (aggressive for free tier)
CACHE_TTL = 1800  # 30 minutes
CACHE_MAX_SIZE = 200

# Input validation
MAX_INPUT_LENGTH = 500
MIN_INPUT_LENGTH = 1

# Personality elements
PERSONALITY_EMOJIS = ["🐾", "😊", "✨", "💙", "🎓"]
CLOSING_PHRASES = [
    "Let me know if you have more questions!",
    "I'm here if you need more help!",
    "Feel free to ask anything else!",
    "Always happy to help, Gentinian!"
]

# Fuzzy matching optimization
CONFIDENCE_THRESHOLD = 0.70  # Minimum confidence for intent match
FUZZY_MATCH_CUTOFF = 0.60    # Lower threshold for fuzzy matching
MAX_PATTERNS_TO_CHECK = 1000  # Limit pattern checking for performance

# Intent matching cache (separate from response cache)
intent_match_cache = {}



# ==============================
# Simple In-Memory Cache
# ==============================
class SimpleCache:
    """Simple LRU cache with TTL for response caching."""
    
    def __init__(self, max_size: int = CACHE_MAX_SIZE, ttl: int = CACHE_TTL):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[str]:
        """Get cached value if exists and not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.ttl):
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return value
            else:
                # Expired, remove
                del self.cache[key]
        return None
    
    def set(self, key: str, value: str):
        """Set cache value with timestamp."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = (value, datetime.now())
        
        # Evict oldest if over max size
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
    
    def clear(self):
        """Clear all cache."""
        self.cache.clear()

response_cache = SimpleCache()

# ==============================
# Rate Limiting
# ==============================
class RateLimiter:
    """Simple rate limiter for API requests."""
    
    def __init__(self, max_requests: int = RATE_LIMIT_REQUESTS, window: int = RATE_LIMIT_WINDOW):
        self.requests = {}
        self.max_requests = max_requests
        self.window = window
    
    def is_allowed(self, user_id: str) -> bool:
        """Check if user is within rate limit."""
        now = datetime.now()
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests outside window
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if now - req_time < timedelta(seconds=self.window)
        ]
        
        # Check if under limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        
        return False

rate_limiter = RateLimiter()

# ==============================
# Load Intents
# ==============================
def load_intents() -> Dict[str, Any]:
    """Load intents from JSON file with error handling."""
    try:
        with open(INTENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ {INTENTS_FILE} loaded successfully ({len(data.get('intents', []))} intents)")
        return data
    except FileNotFoundError:
        print(f"⚠️ {INTENTS_FILE} not found — will rely only on Gemini fallback")
        return {"intents": []}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing {INTENTS_FILE}: {e}")
        return {"intents": []}

intents_data = load_intents()



# ==============================
# Intent Matching Logic (FIXED)
# ==============================
def match_intent(user_message: str) -> Tuple[Optional[str], float]:
    """
    Match user message against intent patterns using optimized fuzzy matching.
    
    OPTIMIZATIONS:
    - Intent match caching for repeated queries
    - Early termination on perfect match
    - Optimized fuzzy matching with cutoff
    - Pattern limit for performance
    
    Args:
        user_message: The user's input message
        
    Returns:
        Tuple of (response, confidence_score) or (None, 0.0) if no match
    """
    normalized_message = user_message.lower().strip()
    
    # Check intent match cache first (separate from response cache)
    cache_key = normalized_message
    if cache_key in intent_match_cache:
        cached_intent, cached_score = intent_match_cache[cache_key]
        if cached_intent:
            # Return fresh random response from cached intent
            return (random.choice(cached_intent.get("responses", [])), cached_score)
        return (None, 0.0)
    
    best_match = None
    best_score = 0.0
    best_response = None
    patterns_checked = 0
    
    for intent in intents_data.get("intents", []):
        patterns = intent.get("patterns", [])
        responses = intent.get("responses", [])
        
        if not patterns or not responses:
            continue
        
        for pattern in patterns:
            # Performance limit
            if patterns_checked >= MAX_PATTERNS_TO_CHECK:
                break
            patterns_checked += 1
            
            pattern_normalized = pattern.lower().strip()
            
            # Exact substring match (fastest)
            if pattern_normalized in normalized_message:
                score = 1.0
                best_score = score
                best_match = intent
                best_response = random.choice(responses)
                # Cache and return immediately on perfect match
                intent_match_cache[cache_key] = (intent, score)
                return (best_response, best_score)
            
            # Fuzzy matching with optimized cutoff
            score = difflib.SequenceMatcher(
                None, 
                normalized_message, 
                pattern_normalized
            ).ratio()
            
            # Update best match if score is higher and above threshold
            if score > best_score and score >= FUZZY_MATCH_CUTOFF:
                best_score = score
                best_match = intent
                best_response = random.choice(responses)
    
    # Cache the result (even if no match)
    if best_score >= CONFIDENCE_THRESHOLD:
        intent_match_cache[cache_key] = (best_match, best_score)
    else:
        intent_match_cache[cache_key] = (None, 0.0)
    
    # Only return if above confidence threshold
    if best_score >= CONFIDENCE_THRESHOLD:
        return (best_response, best_score)
    
    return (None, 0.0)



# ==============================
# Response Formatter
# ==============================
def format_response(text: str, add_personality: bool = True) -> str:
    """
    Format response with Tibby's personality.
    
    Args:
        text: The response text
        add_personality: Whether to add emoji and closing phrase
        
    Returns:
        Formatted response string
    """
    if add_personality and not any(text.startswith(prefix) for prefix in ["⚠️", "❌", "🐾", "😊", "✨", "💙", "🎓"]):
        emoji = random.choice(PERSONALITY_EMOJIS)
        closing = random.choice(CLOSING_PHRASES)
        return f"{emoji} {text} {closing}"
    
    return text

# ==============================
# Input Validation
# ==============================
def validate_input(message: str) -> Tuple[bool, str]:
    """
    Validate user input.
    
    Args:
        message: User's input message
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not message or not message.strip():
        return (False, "⚠️ Please provide a message.")
    
    if len(message) > MAX_INPUT_LENGTH:
        return (False, f"⚠️ Message too long. Please keep it under {MAX_INPUT_LENGTH} characters.")
    
    if len(message.strip()) < MIN_INPUT_LENGTH:
        return (False, "⚠️ Message too short. Please provide a valid question.")
    
    return (True, "")

# ==============================
# Routes
# ==============================
@app.route("/", methods=["GET"])
def home():
    """API status endpoint."""
    return jsonify({
        "message": "Tibby API is running",
        "version": "2.0.0 (Intent-Only)",
        "status": "healthy",
        "intents_loaded": len(intents_data.get("intents", []))
    }), 200

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle chat requests with improved intent matching and Gemini fallback.
    
    Expected JSON: {"message": "user message here"}
    Returns JSON: {"reply": "bot response here", "confidence": 0.95}
    """
    try:
        # Get user IP for rate limiting
        user_ip = request.remote_addr or "unknown"
        
        # Check rate limit
        if not rate_limiter.is_allowed(user_ip):
            return jsonify({
                "reply": "⚠️ Too many requests. Please wait a moment before trying again.",
                "confidence": 0.0
            }), 429
        
        # Validate request
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({
                "reply": "⚠️ Please provide a message in JSON format with a 'message' key.",
                "confidence": 0.0
            }), 400
        
        user_input = data.get("message", "").strip()
        
        # Validate input
        is_valid, error_msg = validate_input(user_input)
        if not is_valid:
            return jsonify({
                "reply": error_msg,
                "confidence": 0.0
            }), 400
        
        # Check cache first
        cache_key = user_input.lower()
        cached_response = response_cache.get(cache_key)
        if cached_response:
            return jsonify({
                "reply": cached_response,
                "confidence": 1.0,
                "cached": True
            }), 200
        
        # Try intent matching with fuzzy logic
        intent_reply, confidence = match_intent(user_input)
        if intent_reply and confidence >= 0.70:
            # Cache the response
            response_cache.set(cache_key, intent_reply)
            return jsonify({
                "reply": intent_reply,
                "confidence": confidence,
                "cached": False
            }), 200
        
        # No match found - provide helpful fallback
        fallback_reply = (
            "🐾 I'm sorry, I don't have information about that yet. "
            "I can help with questions about GTDLNHS like:\n"
            "• Enrollment and admissions\n"
            "• School facilities and location\n"
            "• Schedules and programs\n"
            "• Clubs and organizations\n"
            "• School policies\n\n"
            "What would you like to know about GTDLNHS?"
        )
        return jsonify({
            "reply": fallback_reply,
            "confidence": 0.0
        }), 200
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({
            "reply": "⚠️ Oops! Something went wrong on my end. Please try again!",
            "confidence": 0.0
        }), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint with performance metrics."""
    return jsonify({
        "status": "healthy",
        "intents_loaded": len(intents_data.get("intents", [])),
        "response_cache_size": len(response_cache.cache),
        "intent_cache_size": len(intent_match_cache),
        "total_patterns": sum(len(intent.get("patterns", [])) for intent in intents_data.get("intents", [])),
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route("/cache/clear", methods=["POST"])
def clear_cache():
    """Clear all caches (admin endpoint)."""
    response_cache.clear()
    intent_match_cache.clear()
    return jsonify({
        "message": "All caches cleared successfully",
        "response_cache": "cleared",
        "intent_cache": "cleared",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route("/stats", methods=["GET"])
def stats():
    """Get chatbot statistics."""
    total_patterns = sum(len(intent.get("patterns", [])) for intent in intents_data.get("intents", []))
    avg_patterns = total_patterns / len(intents_data.get("intents", [])) if intents_data.get("intents") else 0
    
    return jsonify({
        "intents": len(intents_data.get("intents", [])),
        "total_patterns": total_patterns,
        "avg_patterns_per_intent": round(avg_patterns, 2),
        "response_cache_size": len(response_cache.cache),
        "intent_cache_size": len(intent_match_cache),
        "cache_max_size": CACHE_MAX_SIZE,
        "cache_ttl_seconds": CACHE_TTL,
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "rate_limit": f"{RATE_LIMIT_REQUESTS} req/min"
    }), 200

# ==============================
# Application Entry Point
# ==============================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Starting Tibby Chatbot Server (v2.0 - Intent-Only)")
    print("="*50)
    print(f"📍 API: http://localhost:5000/")
    print(f"💬 Chat endpoint: POST http://localhost:5000/chat")
    print(f"❤️  Health check: http://localhost:5000/health")
    print(f"📚 Intents loaded: {len(intents_data.get('intents', []))}")
    print(f"🎯 Mode: Pure Intent-Based (No AI API)")
    print(f"🔒 Rate limit: {RATE_LIMIT_REQUESTS} req/min per user")
    print(f"💾 Cache: {CACHE_MAX_SIZE} items, {CACHE_TTL}s TTL")
    print("="*50 + "\n")
    
    app.run(
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )