from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os, random, json, re

app = Flask(__name__)

# ==============================
# Load intents.json
# ==============================
try:
    with open("intents.json", "r", encoding="utf-8") as f:
        intents = json.load(f)
    print("✅ intents.json loaded successfully")
except FileNotFoundError:
    intents = {}
    print("⚠️ intents.json not found — will rely only on Gemini")

# ==============================
# Configure Gemini
# ==============================
try:
    api_key = os.getenv("GEMINI_API_KEY") or "AIzaSyCl-k1r7G4KRj85r4yV6BS8hCEnS8UsjIU"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ Gemini configured successfully")
except Exception as e:
    print(f"❌ Error configuring Gemini: {e}")
    model = None

exceptions_keywords = [
    "math", "calculate", "weather", "joke", "translate", "python", "code",
    "recipe", "news", "sports", "movie", "music"
]

personality_suffixes = [
    " 😊 Let me know if you have more questions!",
    " 🐾 I'm here if you need more help!"
]

# ==============================
# Helper: Match Intent
# ==============================
def match_intent(user_message):
    for intent in intents.get("intents", []):
        for pattern in intent.get("patterns", []):
            if re.search(pattern.lower(), user_message.lower()):
                return random.choice(intent.get("responses", []))
    return None

# ==============================
# Routes
# ==============================
@app.route("/", methods=["GET"])
def home():
    return render_template('tibby.html')

@app.route("/chat", methods=["POST"])
def chat():
    if not model:
        return jsonify({"reply": "⚠️ Chatbot is not properly configured. Check API key."}), 500

    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "⚠️ Please provide a message in JSON format."}), 400
        
        user_input = data.get("message", "").strip()
        if not user_input:
            return jsonify({"reply": "🐾 Hi there! How can I help you today?"}), 200

        # Step 1: Try to match an intent
        intent_reply = match_intent(user_input)
        if intent_reply:
            return jsonify({"reply": f"🐾 {intent_reply}{random.choice(personality_suffixes)}"})

        # Step 2: Fall back to Gemini
        if any(word in user_input.lower() for word in exceptions_keywords):
            prompt = f"You are Tibby, a friendly chatbot.\nQuestion: {user_input}"
        else:
            prompt = f"""
            You are Tibby, the cute chatbot of General Tiburcio de Leon National High School.
            Always answer as if the question is about GTDLNHS unless it clearly matches the exceptions list.
            Keep your tone friendly, concise, and helpful.
            Question: {user_input}
            """

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=120,
                temperature=0.4
            )
        )

        if response and response.text:
            answer = f"🐾 {response.text.strip()}{random.choice(personality_suffixes)}"
        else:
            answer = "⚠️ I couldn't generate a response. Please try again!"
            
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        answer = "⚠️ Oops! Something went wrong. Please try again."

    return jsonify({"reply": answer})

if __name__ == "__main__":
    print("🚀 Starting Tibby chatbot...")
    print("📍 Home: http://localhost:5000/")
    print("💬 Chat endpoint: POST http://localhost:5000/chat")
    app.run(debug=True, host="0.0.0.0", port=5000)
