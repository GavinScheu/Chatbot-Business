"""
Helper script to create a new business chatbot config

Usage: python add_business.py
"""
import os
import json

def create_business_config():
    print("=== Add New Business Chatbot ===\n")
    
    # Get business details
    business_name = input("Business name: ").strip()
    business_id = input("Business ID (lowercase, no spaces, use hyphens): ").strip()
    
    # Create directory
    business_dir = os.path.join('businesses', business_id)
    os.makedirs(business_dir, exist_ok=True)
    
    # Get business info
    print("\nEnter business information (press Enter to skip optional fields):\n")
    
    location = input("Address: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    hours = input("Hours (e.g., 'Mon-Fri 9-5, Sat 10-4'): ").strip()
    
    # Get FAQs
    print("\nEnter your top FAQs (type 'done' when finished):")
    faqs = []
    i = 1
    while True:
        faq = input(f"FAQ {i} (or 'done'): ").strip()
        if faq.lower() == 'done':
            break
        if faq:
            faqs.append(faq)
            i += 1
    
    # Build system prompt
    system_prompt = f"You are the virtual assistant for {business_name}. Your job is to answer customer questions clearly and helpfully.\n\n"
    
    if location:
        system_prompt += f"LOCATION:\n{location}\n\n"
    
    if hours:
        system_prompt += f"HOURS:\n{hours}\n\n"
    
    if phone or email:
        system_prompt += "CONTACT:\n"
        if phone:
            system_prompt += f"Phone: {phone}\n"
        if email:
            system_prompt += f"Email: {email}\n"
        system_prompt += "\n"
    
    if faqs:
        system_prompt += "FREQUENTLY ASKED QUESTIONS:\n"
        for faq in faqs:
            system_prompt += f"- {faq}\n"
        system_prompt += "\n"
    
    system_prompt += f"IMPORTANT: If asked about anything outside your scope, politely direct them to call {phone if phone else 'us'} or visit our website."
    
    # Create config
    config = {
        "business_id": business_id,
        "business_name": business_name,
        "system_prompt": system_prompt,
        "fallback_contact": {
            "phone": phone if phone else "",
            "email": email if email else ""
        },
        "max_tokens": 150
    }
    
    # Save config
    config_path = os.path.join(business_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Created config at: {config_path}")
    print(f"Business ID: {business_id}")
    print("\nNext steps:")
    print("1. Review and edit the config file if needed")
    print("2. Push to GitHub: git add . && git commit -m 'Add new business' && git push")
    print(f"3. Give client embed code with business_id: '{business_id}'")

if __name__ == "__main__":
    create_business_config()