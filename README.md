**📊 Sales Process Automation using Python & AI/ML**
**🔍 Overview**
This project aims to automate the end-to-end sales outreach process using Python and basic AI/ML concepts. It includes data scraping, email campaign automation, lead tracking, and analytics reporting.

✅ **Tasks Breakdown**

  📌 Task 1 & 2: Lead Scraping & Excel Export
        - Scrapes leads from search results (Google, LinkedIn, etc.) based on Ideal Customer 
        - Profile (ICP).   
        - Extracted data includes: company name, website, industry, location, etc. 
        - Outputs to both .xlsx and .csv formats.
  
  📨 Task 3: Email Template Personalization
        - Uses an HTML template with placeholders.
        - Dynamically replaces tags like [Recipient Name], [Company Name], etc., with actual 
          data.
  
  📤 Task 4: Automated Email Campaign
        - Sends personalized emails in batches.
        - Auto-replaces lead emails with dummy addresses (except one real testing email).
        - Supports batching, delay handling, and error-safe delivery.
  
  📈 Task 5: Email Open Tracking & Analytics
        - Implements an open-tracking pixel using a Flask server.
        - Gathers open rates and flags hot vs cold leads based on engagement.
  
🛠️ **Technologies Used**
      Python: Core automation logic
      Libraries: requests, bs4, pandas, openpyxl, smtplib, email, flask
      HTML: Email templating 
      Excel/CSV: Lead data output
      Flask: Tracking pixel analytics server
  
📦 **How to Run**
  Scrape Leads   :Run automation/Task1_2.py to scrape and save leads.
  Generate Emails:Run automation/Task3_email_temp_personalizer.py to create personalized HTML 
                  emails.
  Send Campaign  :Run automation/Task_4_email_sender.py to send emails in batches.
  Track Opens    :Run automation/email_tracker_server.py to start the tracking server.

🎯 **Output Example**
    🗂  Leads: data/SalesLeads_<timestamp>.xlsx
    💌 Email: data/preview_test_email.html
    📊 Analytics: Flask server logs open events


📁 **Project Structure**
Project2/
│
├── automation/
│   ├── Task1_2.py                     # Scrapes data and exports to Excel
│   ├── Task3_email_temp_personalizer.py  # Personalizes HTML email templates
│   ├── Task_4_email_sender.py        # Automates email campaigns with batching
│   ├── create_tracking_pixel.py      # Creates tracking pixel image
│   ├── email_tracker_server.py       # Flask server for tracking email opens
│   └── transparent.gif               # Tracking pixel image
│
├── data/
│   ├── SalesLeads_YYYY-MM-DD.xlsx    # Generated Excel file with leads
│   ├── SalesLeads_YYYY-MM-DD.csv     # CSV version of scraped leads
│   └── preview_test_email.html       # Preview of a sample personalized email
│
└── template/
    └── email_template.html           # Base HTML template with dynamic tags
