# === Task 4 & 5 Integration: Email Sender + Engagement Analytics ===
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
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))
LEADS_FILE = os.path.join(DATA_DIR, "SalesLeads_LATEST.csv")
EMAIL_TEMPLATE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "template", "email_template.html"))
ANALYTICS_OUTPUT_PATH = os.path.join(DATA_DIR, "lead_analytics_report.csv")

# Dummy sender account setup
SENDER_EMAIL = "mca.23.b53@gmail.com"
SENDER_NAME = "Disha (Automation Bot)"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_PASSWORD = "kucn bsfi ojmp qqru"

# Replace with your real email to test only one
REAL_EMAIL = "thakordisha03@gmail.com"

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

def simulate_engagement(leads):
    import random
    leads["Opened"] = [random.choice([True, False]) for _ in range(len(leads))]
    leads["Clicked"] = [random.choice([True, False]) for _ in range(len(leads))]
    leads["Lead Status"] = [
        "Hot Lead" if row.Opened and row.Clicked else "Cold Lead"
        for row in leads.itertuples()
    ]
    return leads

def main():
    if not os.path.exists(LEADS_FILE):
        print(f"❌ Lead file not found at: {LEADS_FILE}")
        return

    template = load_template(EMAIL_TEMPLATE_PATH)
    df = pd.read_csv(LEADS_FILE)

    sent_count = 0
    for index, row in df.iterrows():
        email = REAL_EMAIL if index == 0 else f"dummy{index}@example.com"

        personalized_html = personalize_email(
            template,
            recipient_name=row.get("Contact Person", "there"),
            company_name=row["Company Name"],
            location=row["Location"],
            email=email,
            sender_name="Disha"
        )

        send_email(email, "Let's Collaborate, " + row["Company Name"], personalized_html)

        sent_count += 1
        time.sleep(3)

        if sent_count >= 5:
            break

    df = simulate_engagement(df)
    df.to_csv(ANALYTICS_OUTPUT_PATH, index=False)

    summary = df["Lead Status"].value_counts()
    print("\n🔍 Engagement Summary:")
    print(summary)
    print(f"\n✅ Analytics report saved to: {ANALYTICS_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
