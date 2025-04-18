# === Task 4: send_emails.py ===
import os
import smtplib
import time
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header
from Task3_email_temp_personalizer import load_template, personalize_email

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
LEADS_FILENAME = "SalesLeads_LATEST.csv"
EMAIL_TEMPLATE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "template", "email_template.html"))

# Dummy sender account setup
SENDER_EMAIL = "yourdummyemail@example.com"
SENDER_NAME = "Amit (Automation Bot)"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASSWORD = "your_dummy_password"

# Replace with your real email to test only one
REAL_EMAIL = "youremail@example.com"


def send_email(to_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(SENDER_NAME, 'utf-8')), SENDER_EMAIL))
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        print(f"✅ Email sent to: {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")


def main():
    leads_path = os.path.join(LEADS_FILE, LEADS_FILENAME)
    if not os.path.exists(leads_path):
        print(f"❌ Lead file not found at: {leads_path}")
        return

    template = load_template(EMAIL_TEMPLATE_PATH)
    df = pd.read_csv(leads_path)

    sent_count = 0
    for index, row in df.iterrows():
        email = REAL_EMAIL if index == 0 else f"dummy{index}@example.com"

        personalized_html = personalize_email(
            template,
            recipient_name=row.get("Contact Person", "there"),
            company_name=row["Company Name"],
            location=row["Location"],
            email=email,
            sender_name="Amit"
        )

        send_email(email, "Let's Collaborate, " + row["Company Name"], personalized_html)

        sent_count += 1
        time.sleep(3)  # Delay to avoid spam detection

        if sent_count >= 5:
            break


if __name__ == "__main__":
    main()


# === Task 5: analyze_engagement.py ===
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "SalesLeads_LATEST.csv"))
ANALYTICS_OUTPUT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "lead_analytics_report.csv"))

# Simulate engagement (in a real case this comes from pixel tracking or ESP APIs)
def simulate_engagement(leads):
    import random
    leads["Opened"] = [random.choice([True, False]) for _ in range(len(leads))]
    leads["Clicked"] = [random.choice([True, False]) for _ in range(len(leads))]
    leads["Lead Status"] = [
        "Hot Lead" if row.Opened and row.Clicked else "Cold Lead"
        for row in leads.itertuples()
    ]
    return leads


def generate_report():
    if not os.path.exists(DATA_PATH):
        print("❌ Data not found. Run scraping first.")
        return

    df = pd.read_csv(DATA_PATH)
    df = simulate_engagement(df)
    df.to_csv(ANALYTICS_OUTPUT_PATH, index=False)

    summary = df["Lead Status"].value_counts()
    print("\n🔍 Engagement Summary:")
    print(summary)
    print(f"\n✅ Report saved to: {ANALYTICS_OUTPUT_PATH}")


if __name__ == '__main__':
    generate_report()



# import pandas as pd
# import smtplib
# import time
# import re
# import os
# import subprocess
# import requests
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from Task3_email_temp_personalizer import load_template, personalize_email

# # === CONFIGURATION ===
# DATA_DIR = r"C:/Users/Hp/.spyder-py3/my_programs/Project2/data"
# EMAIL_TEMPLATE_PATH = "C:/Users/Hp/.spyder-py3/my_programs/Project2/templates/email_template.html"
# TRACKING_SERVER = "http://localhost:5000/track"
# TRACKING_SERVER_PING = "http://localhost:5000/"
# REAL_EMAIL = "mca.23.b53@gmail.com"
# DUMMY_EMAIL_DOMAIN = "dummyemail.com"
# SUBJECT = "Boost Your Sales Process with Automation 🚀"
# SENDER_EMAIL = REAL_EMAIL
# SENDER_PASSWORD = "kucn bsfi ojmp qqru"
# DELAY_BETWEEN_EMAILS = 5  # seconds

# # === Get Latest Excel File ===
# def get_latest_excel_file(directory):
#     files = [f for f in os.listdir(directory) if f.startswith("SalesLeads_") and f.endswith(".xlsx")]
#     if not files:
#         raise FileNotFoundError("❌ No SalesLeads_*.xlsx files found in the data directory.")
#     files.sort(reverse=True)
#     return os.path.join(directory, files[0])

# # === Email Validation ===
# def is_valid_email(email):
#     pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
#     return re.match(pattern, email)

# # === Load Leads from Excel ===
# def load_leads(filepath):
#     df = pd.read_excel(filepath)
#     leads = []
#     for idx, row in df.iterrows():
#         email = row.get("Email", "")
#         if not is_valid_email(email):
#             continue
#         # Replace all emails with dummy, except your real one
#         if email != REAL_EMAIL:
#             email = f"lead{idx}@{DUMMY_EMAIL_DOMAIN}"
#         leads.append({
#             "email": email,
#             "name": row.get("Contact Person", "there"),
#             "company": row.get("Company Name", "your company"),
#             "location": row.get("Location", "your region")
#         })
#     return leads

# # === Send One Email ===
# def send_email(smtp_server, sender_email, recipient_email, subject, html_body):
#     msg = MIMEMultipart("alternative")
#     msg["Subject"] = subject
#     msg["From"] = sender_email
#     msg["To"] = recipient_email
#     part = MIMEText(html_body, "html")
#     msg.attach(part)
#     smtp_server.sendmail(sender_email, recipient_email, msg.as_string())

# # === Auto-Start Tracker Server if Not Running ===
# def ensure_tracking_server_running():
#     try:
#         requests.get(TRACKING_SERVER_PING, timeout=2)
#         print("🟢 Tracking server already running.")
#     except Exception:
#         print("🟡 Starting tracking server...")
#         tracker_script = os.path.join(os.path.dirname(__file__), "email_tracker_server.py")
#         subprocess.Popen(["python", tracker_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         time.sleep(2)  # Give time to start

# # === Main Campaign Function ===
# def run_campaign():
#     ensure_tracking_server_running()

#     try:
#         excel_file = get_latest_excel_file(DATA_DIR)
#         print(f"📁 Using latest Excel file: {excel_file}")
#     except FileNotFoundError as e:
#         print(e)
#         return

#     print("📥 Loading leads...")
#     leads = load_leads(excel_file)
#     if not leads:
#         print("⚠️ No valid leads found.")
#         return

#     print(f"✅ {len(leads)} valid leads loaded.")
#     print("📄 Loading email template...")
#     template = load_template(EMAIL_TEMPLATE_PATH)

#     print("📨 Connecting to Gmail SMTP...")
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         return

#     print("🚀 Starting email campaign...\n")

#     for i, lead in enumerate(leads, start=1):
#         tracking_pixel = f'<img src="{TRACKING_SERVER}?email={lead["email"]}&event=open" width="1" height="1" />'
#         personalized_html = personalize_email(
#             template,
#             recipient_name=lead["name"],
#             company_name=lead["company"],
#             location=lead["location"],
#             email=lead["email"],
#             sender_name="Your Name"
#         ) + tracking_pixel

#         try:
#             send_email(server, SENDER_EMAIL, lead["email"], SUBJECT, personalized_html)
#             print(f"✅ Sent to {lead['email']} ({lead['company']})")
#         except Exception as e:
#             print(f"❌ Failed to send to {lead['email']}: {e}")

#         if i < len(leads):
#             print(f"⏳ Waiting {DELAY_BETWEEN_EMAILS} seconds...\n")
#             time.sleep(DELAY_BETWEEN_EMAILS)

#     server.quit()
#     print("\n🎉 Campaign complete!")

# # === Run the Campaign ===
# if __name__ == "__main__":
#     run_campaign()
