import pandas as pd
import smtplib
import time
import re
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Task3_email_temp_personalizer import load_template, personalize_email

# === CONFIGURATION ===
DATA_DIR = r"C:/Users/Hp/.spyder-py3/my_programs/Project2/data"
EMAIL_TEMPLATE_PATH = "C:/Users/Hp/.spyder-py3/my_programs/Project2/templates/email_template.html"
TRACKING_SERVER = "http://127.0.0.1:5000/track"

SENDER_EMAIL = "mca.23.b53@gmail.com"
SENDER_PASSWORD = "kucn bsfi ojmp qqru"  # App password
SUBJECT = "Boost Your Sales Process with Automation 🚀"
DELAY_BETWEEN_EMAILS = 5  # seconds

# === Get Latest Excel File ===
def get_latest_excel_file(directory):
    files = [f for f in os.listdir(directory) if f.startswith("SalesLeads_") and f.endswith(".xlsx")]
    if not files:
        raise FileNotFoundError("❌ No SalesLeads_*.xlsx files found in the data directory.")
    files.sort(reverse=True)
    return os.path.join(directory, files[0])

# === Email Validation ===
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# === Load Leads from Excel ===
def load_leads(filepath):
    df = pd.read_excel(filepath)
    leads = []
    for _, row in df.iterrows():
        if is_valid_email(row.get("Email", "")):
            leads.append({
                "email": row["Email"],
                "name": row.get("Contact Person", "there"),
                "company": row.get("Company Name", "your company"),
                "location": row.get("Location", "your region")
            })
    return leads

# === Send One Email ===
def send_email(smtp_server, sender_email, recipient_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    part = MIMEText(html_body, "html")
    msg.attach(part)
    smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

# === Main Campaign Function ===
def run_campaign():
    try:
        excel_file = get_latest_excel_file(DATA_DIR)
        print(f"📁 Using latest Excel file: {excel_file}")
    except FileNotFoundError as e:
        print(e)
        return

    print("📥 Loading leads...")
    leads = load_leads(excel_file)
    if not leads:
        print("⚠️ No valid leads found.")
        return

    print(f"✅ {len(leads)} valid leads loaded.")
    print("📄 Loading email template...")
    template = load_template(EMAIL_TEMPLATE_PATH)

    print("📨 Connecting to Gmail SMTP...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return

    print("🚀 Starting email campaign...\n")

    for i, lead in enumerate(leads, start=1):
        tracking_pixel = f'<img src="{TRACKING_SERVER}?email={lead["email"]}&event=open" width="1" height="1" />'

        personalized_html = personalize_email(
            template,
            recipient_name=lead["name"],
            company_name=lead["company"],
            location=lead["location"],
            email=lead["email"],
            sender_name="Your Name"
        ) + tracking_pixel

        try:
            send_email(server, SENDER_EMAIL, lead["email"], SUBJECT, personalized_html)
            print(f"✅ Sent to {lead['email']} ({lead['company']})")
        except Exception as e:
            print(f"❌ Failed to send to {lead['email']}: {e}")

        if i < len(leads):
            print(f"⏳ Waiting {DELAY_BETWEEN_EMAILS} seconds...\n")
            time.sleep(DELAY_BETWEEN_EMAILS)

    server.quit()
    print("\n🎉 Campaign complete!")

    # Debug: Notify tracking will now be logged from email opens
    print("📊 Email open tracking will be stored in email_tracking_log.csv by the server.")

# === Run the Campaign ===
if __name__ == "__main__":
    run_campaign()
