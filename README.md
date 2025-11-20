
## Project Overview: Apparel Store Platform

This codebase is an apparel store web application featuring a recommendation system and personalized email generation for new product launches using Google Generative AI (Gemini).

### Key Features

- **Product Catalog:** Browse products, variants, and inventory.
- **Recommendation System:** Suggests product combinations and alternatives based on user queries and product variants.
- **Personalized Email Generation:** Uses Google Generative AI (Gemini) to create tailored HTML emails for customers about new product launches, considering their preferences and profile.
- **Customer Management:** Handles customer personal data, preferences, addresses, and meta information.
- **Order Management:** Supports order headers, items, and offer usage tracking.
- **Admin Dashboard:** Admin page for managing products and viewing analytics.
- **Bulk Data Import:** Loads initial data from CSV files for products, customers, inventory, etc.
- **Modern Web UI:** Uses Jinja2 templates and static assets for a user-friendly interface.

### Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **AI Integration:** Google Generative AI (Gemini) for email content
- **Frontend:** Jinja2 templates, HTML, CSS, JavaScript
- **Data Import:** CSV bulk loading via Python scripts
- **Email Sending:** SMTP (Gmail)
- **Other Libraries:** pandas, psycopg2, dateutil, smtplib

### Recommendation System

- Generates product combos and suggestions using custom logic (`combo_logic.py`).
- API endpoints provide recommendations based on product queries and variants.

### Personalized Email Generation

- For new product launches, the system matches products to customer preferences.
- Uses Gemini AI to generate engaging, personalized HTML emails.
- Emails are sent via Gmail SMTP to opted-in customers.

---

**Summary:**  
This apparel store platform combines e-commerce features with AI-powered personalization, offering smart recommendations and automated, tailored email marketing for enhanced customer engagement.
