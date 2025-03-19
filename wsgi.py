from flask import Flask, request, jsonify
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

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the user message from the request
        data = request.json
        user_message = data.get("message", "").strip()

        # **Limit User Input Size**
        if len(user_message) > 500:
            return jsonify({"reply": "Error: Your message is too long. Please keep it under 500 characters."}), 400

        # Call OpenAI API with GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=50
        )

        # Extract chatbot reply
        chatbot_reply = response.choices[0].message.content.strip()

        return jsonify({"reply": chatbot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message for debugging

# Render requires Flask to listen on port 10000
def main():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()
