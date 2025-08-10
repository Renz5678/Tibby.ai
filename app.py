from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import random

app = Flask(__name__)

# Configure Gemini/Gemma model
genai.configure(api_key="AIzaSyCl-k1r7G4KRj85r4yV6BS8hCEnS8UsjIU")
model = genai.GenerativeModel("gemma-3-1b-it")

# Refined and shorter school context
SCHOOL_CONTEXT = (
    "You are Tibby, a helpful and friendly chatbot for General Tiburcio de Leon National High School (GTDLNHS), "
    "located in Valenzuela City, Metro Manila.\n"
    "Only answer questions related to GTDLNHS. If the message is not about the school, respond with: "
    "'I'm sorry, but I can only answer questions about General Tiburcio de Leon National High School.'\n"
    "\n"
    "📍 School Facts:\n"
    "- Name: General Tiburcio de Leon National High School (GTDLNHS)\n"
    "- Founded: 1969; became independent in 1997\n"
    "- Address: Mercado St. corner Gen. T. de Leon Road, Brgy. Gen. T. de Leon, Valenzuela City\n"
    "- Principal: Mr. Eddie Alarte\n"
    "- Grade Levels: Grade 7 to Grade 12\n"
    "- Curriculum: New DepEd-aligned curriculum\n"
    "- Senior High Program: Strengthened Senior High School Program with career pathways:\n"
    "   * Bakery Operations\n"
    "   * Business and Entrepreneurship\n"
    "   * Creative and Multimedia Arts\n"
    "   * Culinary Arts\n"
    "   * Engineering\n"
    "   * Food and Beverage Services\n"
    "   * Health Sciences\n"
    "   * Hospitality and Tourism\n"
    "   * Social Science and Humanities\n"
    "   * Software Development\n"
    "- Special Programs: Special Education (SPED) for learners with special needs\n"
    "- Campus: 39 rooms, 4 floors, covered court, new amphitheater (2024)\n"
    "\n"
    "📌 Admissions:\n"
    "- Enroll at Registrar’s Office (Building A) with PSA Birth Certificate, Report Card (SF9), and Good Moral Certificate\n"
    "- No entrance exam required\n"
    "- Transferees accepted until end of second quarter\n"
    "\n"
    "🗓 School Year & Schedule:\n"
    "- Starts in June\n"
    "- Grade 7: 6:00 AM – 12:30 PM\n"
    "- Grade 8: 12:40 PM – 7:00 PM\n"
    "- Grade 9: 1:00 PM – 7:20 PM\n"
    "- Grade 10: 6:00 AM – 12:40 PM\n"
    "- Grade 11: 6:00 AM – 12:30 PM\n"
    "- Grade 12: 12:45 PM – 7:30 PM\n"
    "\n"
    "🏫 Facilities:\n"
    "- Comfort Rooms\n"
    "- Computer Laboratory\n"
    "- Faculty Room\n"
    "- Guidance Office\n"
    "- Library\n"
    "- Multi-purpose Hall\n"
    "- School Canteen\n"
    "- School Clinic\n"
    "- Science Laboratory\n"
    "\n"
    "🎯 Student Life:\n"
    "- Clubs & Organizations: Ang Daluyan, Ecosavers Club, English Club, ESP Club, Junior’s Computers Club, Language Club, "
    "Library Club, Math Club, Nexus Club, Science Club, Sipnayan Club, Siyensaya Club, Social Science Club, "
    "The Genzette, TLE Club\n"
    "- Guidance & Counseling available\n"
    "- Uniform required (JHS: Mon–Thu uniform, Fri P.E.; SHS: uniform except on HOPE class day for P.E.)\n"
    "\n"
    "📞 Contact:\n"
    "- Phone: 0967-023-7047\n"
    "- Email: gtdlnhs2007@gmail.com\n"
    "- Facebook: https://www.facebook.com/share/1BMPoam8K2/?mibextid=wwXIfr\n"
    "\n"
    "💡 Other Info:\n"
    "- Open High School available for students with health concerns\n"
    "- Parents updated via class GCs & official FB page\n"
    "- Card distribution is the official way to view grades\n"
    "- Work Immersion required for SHS graduation\n"
    "- Moving up & graduation require completion of academic requirements and good moral standing\n"
    "- Bullying incidents should be reported to adviser or Guidance Office\n"
    "- Lost IDs must be reported for replacement\n"
    "- SSG candidacy: Contact Sir Arnielson Calubiran or visit SSLG HQ\n"
    "- Class suspensions announced via official channels"
)

# Keywords to detect school-related messages
school_keywords = [
    "tiburcio", "gtdlnhs", "gtdl", "enrollment", "principal", "grades", "junior high",
    "senior high", "shs", "jhs", "uniform", "school id", "schedule", "strand", "section",
    "requirements", "school year", "student", "teacher", "campus", "building", "classroom",
    "event", "sslg", "address", "location", "map", "how do i get there", "where is",
    "where are you located", "hello", "hi", "contact", "phone", "facebook", "immersion",
    "spes", "sped", "club", "organization", "ssg", "guidance", "card distribution"
]

# Friendly personality suffixes
personality_suffixes = [
    " 😊 Let me know if you have more questions!",
    " 🐾 I'm here if you need more help!",
    " 🎓 Hope that answered your question, superstar!",
    " 🌟 Just ask away if you're curious about anything else!",
    " 💬 Always happy to help, Gentinian!"
]


@app.route("/")
def home():
    return render_template("tibby.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip().lower()

    if not user_input:
        return jsonify({"reply": "Please enter a valid message. 🧐"}), 400

    if user_input in ["hi", "hello", "hey"]:
        return jsonify({
            "reply": "👋 Hello, Gentinian! I am Tibby, GTDLNHS' cutest chatbot. How may I help you today?"
        })

    if any(phrase in user_input for phrase in ["thank you", "thanks", "ty", "thank u", "salamat", "arigato", "much obliged"]):
        return jsonify({
            "reply": "You're most welcome! 🐾 I'm always here to help, Gentinian!"
        })

    if not any(keyword in user_input for keyword in school_keywords):
        return jsonify({
            "reply": "😅 I'm sorry, but I can only answer questions about General Tiburcio de Leon National High School."
        })

    # Construct the prompt with concise answer instruction
    prompt = (
        f"{SCHOOL_CONTEXT}\n\n"
        f"Answer the following question in a friendly, concise, and informative tone:\n"
        f"Question: {user_input}\n"
        f"Answer:"
    )

    try:
        # Generate content with token and temperature control
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=100,
                temperature=0.4
            )
        )
        raw_reply = response.text.strip()
        suffix = random.choice(personality_suffixes)
        final_reply = f"🐾 {raw_reply}{suffix}"
    except Exception as e:
        print("Gemini error:", e)
        final_reply = "⚠️ Oops! Tibby encountered a small hiccup. Please try again."

    return jsonify({"reply": final_reply})

if __name__ == "__main__":
    app.run(debug=True)
