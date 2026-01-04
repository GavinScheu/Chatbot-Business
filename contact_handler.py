"""
Contact form handler for BizChatAssist
Sends contact form submissions to mjm0208@auburn.edu
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_contact_email(business_name, email, phone, message):
    """
    Send contact form data via email to gavinscheu@gmail.com
    
    Args:
        business_name: Name of the business
        email: Contact email (optional)
        phone: Contact phone (optional)
        message: Additional message from contact
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Get SMTP credentials from environment variables
    smtp_email = os.getenv('SMTP_EMAIL')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not smtp_email or not smtp_password:
        print("ERROR: SMTP credentials not configured")
        return False
    
    # Create email content
    subject = f"New BizChatAssist Inquiry: {business_name}"
    
    body = f"""
New Contact Form Submission from BizChatAssist.com

Business Name: {business_name}
Email: {email if email else 'Not provided'}
Phone: {phone if phone else 'Not provided'}

Message:
{message if message else 'No additional message'}

---
Received via bizchatassist.com contact form
"""
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_email
    msg['To'] = 'gavinscheu@gmail.com'
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        
        print(f"Contact form email sent successfully for {business_name}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False