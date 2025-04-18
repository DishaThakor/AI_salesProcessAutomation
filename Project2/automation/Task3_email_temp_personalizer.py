import os

# === Constants ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# TEMPLATE_PATH = "templates/email_template.html"
# SAVE_PREVIEW_PATH = r"C:/Users/Hp/.spyder-py3/my_programs/Project2/data/test_output_email.html"

TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "template", "email_template.html")
SAVE_PREVIEW_PATH = os.path.join(BASE_DIR, "..", "data", "preview_test_email.html")

def load_template(filepath=TEMPLATE_PATH):
    """Loads the HTML email template."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Email template not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def personalize_email(template, recipient_name, company_name, location, email, sender_name):
    """Fills placeholders with actual data from leads."""
    return (template
            .replace("[Recipient Name]", recipient_name)
            .replace("[Company Name]", company_name)
            .replace("[Location]", location)
            .replace("[Email]", email)
            .replace("[Your Name]", sender_name))

# --- Test Usage ---
if __name__ == "__main__":
    try:
        test_data = {
            "recipient_name": "John Doe",
            "company_name": "NextGen Tech",
            "location": "Mumbai",
            "email": "dummy@example.com",
            "sender_name": "Amit"
        }

        template = load_template()
        personalized = personalize_email(template, **test_data)

        os.makedirs(os.path.dirname(SAVE_PREVIEW_PATH), exist_ok=True)
        with open(SAVE_PREVIEW_PATH, "w", encoding="utf-8") as f:
            f.write(personalized)

        print(f"✅ Email preview saved to: {SAVE_PREVIEW_PATH}")

    except Exception as e:
        print(f"❌ Error: {e}")

# import os

# # === CONSTANTS ===
# TEMPLATE_PATH = "templates/email_template.html"
# SAVE_PREVIEW_PATH = r"C:/Users/Hp/.spyder-py3/my_programs/Project2/data/test_output_email.html"

# def load_template(filepath=TEMPLATE_PATH):
#     """Loads the HTML email template."""
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"Email template not found at: {filepath}")
#     with open(filepath, "r", encoding="utf-8") as file:
#         return file.read()

# def personalize_email(template, recipient_name, company_name, location, email, sender_name):
#     """Fills placeholders with actual data."""
#     return (template
#             .replace("[Recipient Name]", recipient_name)
#             .replace("[Company Name]", company_name)
#             .replace("[Location]", location)
#             .replace("[Email]", email)
#             .replace("[Your Name]", sender_name))

# # --- Demo/Test Usage ---
# if __name__ == "__main__":
#     recipient_name = "John Doe"
#     company_name = "NextGen Tech"
#     location = "Mumbai"
#     email = "dummy@example.com"
#     sender_name = "Amit"

#     try:
#         template = load_template()
#         personalized_html = personalize_email(template, recipient_name, company_name, location, email, sender_name)

#         with open(SAVE_PREVIEW_PATH, "w", encoding="utf-8") as preview:
#             preview.write(personalized_html)

#         print(f"✅ Email preview saved as '{SAVE_PREVIEW_PATH}'")
#     except Exception as e:
#         print(f"❌ Error: {e}")
