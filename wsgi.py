from flask import Flask, request, jsonify
from flask_cors import CORS
from contact_handler import send_contact_email
import openai
import os
import json
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

# Load all business configurations
BUSINESSES = {}

def load_business_configs():
    """Load all business configs from the businesses/ directory"""
    # Try multiple possible paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), 'businesses'),
        os.path.join(os.getcwd(), 'businesses'),
        'businesses'
    ]
    
    businesses_dir = None
    for path in possible_paths:
        if os.path.exists(path):
            businesses_dir = path
            break
    
    if not businesses_dir:
        print("ERROR: businesses/ directory not found in any expected location")
        print(f"Tried: {possible_paths}")
        print(f"Current dir: {os.getcwd()}")
        print(f"Files in current dir: {os.listdir('.')}")
        return
    
    print(f"Loading businesses from: {businesses_dir}")
    
    for business_folder in os.listdir(businesses_dir):
        folder_path = os.path.join(businesses_dir, business_folder)
        if not os.path.isdir(folder_path):
            continue
            
        config_path = os.path.join(folder_path, 'config.json')
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    business_id = config.get('business_id')
                    BUSINESSES[business_id] = config
                    print(f"✓ Loaded config for: {config.get('business_name')} (ID: {business_id})")
            except Exception as e:
                print(f"✗ Error loading config for {business_folder}: {e}")

# Load configs on startup
load_business_configs()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get the user message and business ID from the request
        data = request.json
        user_message = data.get("message", "").strip()
        business_id = data.get("business_id", "marios-italian")  # Default to Mario's for demo
        
        # Limit User Input Size
        if len(user_message) > 500:
            return jsonify({"reply": "Error: Your message is too long. Please keep it under 500 characters."}), 400
        
        # Get business config
        business_config = BUSINESSES.get(business_id)
        
        if not business_config:
            return jsonify({"error": f"Business '{business_id}' not found"}), 404
        
        # Get system prompt and settings from config
        system_prompt = business_config.get("system_prompt")
        max_tokens = business_config.get("max_tokens", 100)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=max_tokens
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

# Render requires Flask to listen on port 10000
def main():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()