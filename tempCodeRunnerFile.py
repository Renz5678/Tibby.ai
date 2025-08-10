from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini / Gemma API
genai.configure(api_key="YOUR_API_KEY")  # Replace with your valid API key
model = genai.GenerativeModel("gemma-3-1b-it")

# Static school info for prompt injection
SCHOOL_CONTEXT = (
    "You are a chatbot for General Tiburcio de Leon National High School (GTDLNHS) in Valenzuela City, Metro Manila.\n"
    "Facts:\n"
    "- Official name: General Tiburcio de Leon National High School (GTDLNHS)\n"
    "- Founded: 1969; independent since 1997\n"
    "- Address: Mercado St. cor. Gen. T. de Leon Road, Brgy. Gen. T. de Leon, Valenzuela City\n"
    "- Principal: Mr. Eddie Alarte\n"
    "- Grades: 7–12; approx. 50 students per class; student–teacher ratio ~50:1\n"
    "- Campus: urban; four-storey main building (39 rooms) and covered court\n"
    "- September 2024: Expansion funded by San Miguel Corp — 16-classroom building + amphitheater\n"
    "- June 9, 2025: SSLG inauguration event held\n"
    "- Strands for Grade 12 are STEM, HUMSS, ICT, GAS, ABM, TVL-ICT, TVL-HE, TVL-Tourism\n"
    "Answer concisely and only about GTDLNHS. If unrelated, reply: "
    "“I’m sorry, but I can only answer questions about General Tiburcio de Leon National High School.”\n\n"
)

school_keywords = [
    "tiburcio", "gtdlnhs", "enrollment", "principal", "grade", "section",
    "strand", "uniform", "class schedule", "school id", "student", "teacher",
    "subject", "senior high", "junior high", "school year", "requirement", "located"
]

# In-memory chat history (optional)
history = []

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter a valid message."}), 400

    # Keyword filtering
    if not any(keyword in user_input.lower() for keyword in school_keywords):
        return jsonify({
            "reply": "I’m sorry, but I can only answer questions about General Tiburcio de Leon National High School."
        })

    # Build the prompt with context
    history.append(f"User: {user_input}")
    prompt = SCHOOL_CONTEXT + "\nUser: " + user_input + "\nAssistant:"
    response = model.generate_content(prompt)
    reply = response.text.strip()
    history.append(f"Assistant: {reply}")

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
