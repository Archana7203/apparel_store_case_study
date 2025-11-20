import smtplib
import google.generativeai as genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from db import db
from models import CustomerMeta, CustomerPersonal, CustomerPreference
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def normalize_gender(val):
    val = str(val).strip().lower()
    if val in ["men", "male"]:
        return "men"
    if val in ["women", "female"]:
        return "women"
    if val == "unisex":
        return "unisex"
    return val

def build_prompt(row, product):
    return f"""
    You are a creative fashion email assistant powered by Gemini. Your goal is to generate a **highly personalized HTML email body** that introduces a new product launch to a customer in an engaging, friendly, and stylish way.

    Personalize every part of the message based on the customer's preferences and personality. Make the customer feel seen and valued.

    ---

    **Customer Details**:
        - Name: {row['first_name']} {row['last_name']}
        - Style Preference: {row['style_preference_1']}
        - Favorite Color: {row['style_preference_2']}
        - Favorite Brand: {row['style_preference_3']}
        - Gender: {row['gender']}
        - Preferred Language: {row['preferred_language']}

    **Product Details**:
        - Name: {product['name']}
        - Brand: {product['brand']}
        - Color: {product['color']}
        - Style: {product['style']}
        - Description: {product['description']}
        - Product Page URL: {product['image']}
        - Product Image URL: {product['image']}

    ---

    **Email Requirements**:
        - Write in **HTML** format only.
        - Tone: Friendly, stylish, personalized, and emotionally engaging.
        - Structure: Short, creative paragraphs that read like a fashion magazine snippet.
        - Use stylish and relevant emojis such as ✨🛍️👗👚👖👟👜❤️🎉🔥 to add energy and warmth.
        - “Use <b>bold</b> HTML tags for product names, special phrases, and calls-to-action (CTAs). Do not use Markdown asterisks.” 
        - Use attractive headings and formatting (e.g., relevant color text, spacing, playful tone) to make the email visually appealing.
        - Highlight why this product matches the customer's preferences (style, color, brand).
        - Include a <b>Shop Now</b> CTA button or link to the product page.
        - Add the product image (200x200 px).

    ---

    **Goal**:
        Delight the customer with a vibrant, eye-catching, and irresistibly clickable email that feels tailored just for them. Every word and emoji should reflect the customer's unique taste and make them excited to explore the product.
    """

def send_email(to_email, subject, html_content):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_SENDER"), os.getenv("APP_PASSWORD"))
        server.send_message(msg)

def get_target_customers(product):
    style = str(product["style"]).strip().lower()
    color = str(product["color"]).strip().lower()
    brand = str(product["brand"]).strip().lower()
    product_gender = normalize_gender(product.get("gender", "Unisex"))

    # Query joined customer data from DB
    customers = db.query(CustomerPreference, CustomerPersonal)
    customers = customers.join(CustomerPersonal, CustomerPreference.customer_id == CustomerPersonal.customer_id)
    customers = customers.filter(CustomerPreference.marketing_opted_in == True)
    customers = customers.filter(CustomerPreference.style_preference_1.ilike(style))
    customers = customers.filter(
        (CustomerPreference.style_preference_2.ilike(color)) |
        (CustomerPreference.style_preference_3.ilike(brand))
    )
    if product_gender != "unisex":
        customers = customers.filter(CustomerPersonal.gender.ilike(product_gender))
    # Build result rows as dicts
    result = []
    for pref, personal in customers:
        # Find email column
        email_val = getattr(personal, "email", None) or getattr(personal, "email_id", None)
        if not email_val:
            continue
        row = {
            "first_name": personal.first_name,
            "last_name": personal.last_name,
            "email": email_val,
            "style_preference_1": pref.style_preference_1,
            "style_preference_2": pref.style_preference_2,
            "style_preference_3": pref.style_preference_3,
            "gender": personal.gender,
            "preferred_language": personal.preferred_language,
        }
        result.append(row)
    return result, "email"

def process_and_send_emails(product):
    recipients = []
    try:
        target_customers, email_col = get_target_customers(product)
        for row in target_customers:
            email_val = row[email_col]
            if not isinstance(email_val, str) or '@' not in email_val:
                continue
            prompt = build_prompt(row, product)
            response = model.generate_content(prompt)
            html = response.text
            subject = f"✨ {product['name']} Just Dropped!"
            send_email(email_val, subject, html)
            recipients.append(f"{row['first_name']} {row['last_name']} <{email_val}>")
        return recipients
    except Exception as e:
        raise e
