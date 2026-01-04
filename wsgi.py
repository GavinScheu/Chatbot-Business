from flask import Flask, request, jsonify
from flask_cors import CORS
from contact_handler import send_contact_email
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is loaded properly
if not api_key:
    raise ValueError("Error: OPENAI_API_KEY not found. Make sure you have a .env file with the correct API key.")

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the user message from the request
        data = request.json
        user_message = data.get("message", "").strip()

        # Limit User Input Size
        if len(user_message) > 500:
            return jsonify({"reply": "Error: Your message is too long. Please keep it under 500 characters."}), 400

        # Call OpenAI API with GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the virtual assistant for Will's Waste, LLC — a local, family-owned waste collection company "
                        "serving Coal Mountain, Silver City, and Matt in Forsyth County, Georgia. "
                        "Your job is to answer customer questions clearly and helpfully about trash pickup options, pricing, "
                        "and how to sign up. "
                        "Pricing: $30/month for curbside, $40/month for backdoor, $10 per extra container, bulk pickup available by request. "
                        "If asked something outside your scope, politely direct them to call 770-762-WILL (9455) or visit https://willswaste.com."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=100
        )

        # Extract chatbot reply
        chatbot_reply = response.choices[0].message.content.strip()

        return jsonify({"reply": chatbot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.json
        business_name = data.get("business_name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        message = data.get("message", "").strip()
        
        # Validate business name is provided
        if not business_name:
            return jsonify({"error": "Business name is required"}), 400
        
        # Validate at least one contact method
        if not email and not phone:
            return jsonify({"error": "Email or phone required"}), 400
        
        # Send email
        success = send_contact_email(business_name, email, phone, message)
        
        if success:
            return jsonify({"message": "Contact form submitted successfully"}), 200
        else:
            return jsonify({"error": "Failed to send email"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def main():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()