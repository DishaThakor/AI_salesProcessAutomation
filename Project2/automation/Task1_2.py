import customtkinter as ctk
from googlesearch import search
from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import re
import threading
import os
import chardet
import csv
import time
import random
from fake_useragent import UserAgent
import subprocess  # For opening folder

latest_file = ""
save_dir = r"C:/Users/Hp/.spyder-py3/my_programs/Project2/data"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def open_csv(filename):
    try:
        os.startfile(filename)
    except Exception as e:
        log_label.configure(text=f"⚠️ Could not open file: {e}", text_color="red")

# def open_folder():
#     try:
#         subprocess.Popen(f'explorer "{save_dir}"')
#     except Exception as e:
#         log_label.configure(text=f"⚠️ Could not open folder: {e}", text_color="red")

def clean_company_name(raw_title):
    noise_words = [
        "Best", "Top", "Website", "Services", "in", "India",
        "Ahmedabad", "Firm", "Agency", "Developer", "SEO"
    ]
    for word in noise_words:
        raw_title = re.sub(rf"\b{word}\b", "", raw_title, flags=re.IGNORECASE)
    raw_title = re.sub(r'\s+', ' ', raw_title).strip()
    
    match = re.findall(r'[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', raw_title)
    if match:
        return match[-1].strip()
    return raw_title

def is_valid_company_name(name):
    return bool(re.match(r'^[a-zA-Z0-9 &.\'-]{2,}$', name)) and not re.fullmatch(r'[^a-zA-Z0-9]+', name)

def scrape_companies():
    industry = entry_industry.get()
    location = entry_location.get()

    if not industry or not location:
        log_label.configure(text="❗ Please enter both industry and location.", text_color="red")
        return

    log_label.configure(text="🔄 Scraping in progress...", text_color="orange")
    progress_bar.set(0)
    app.update()

    query = f"{industry} companies in {location}"
    result_list = []

    try:
        urls = list(search(query, stop=20))
    except Exception as e:
        log_label.configure(text=f"❌ Google Search Failed: {e}", text_color="red")
        return

    total = len(urls)
    ua = UserAgent()

    for i, url in enumerate(urls):
        try:
            if any(bad in url for bad in ["linkedin.com", "facebook.com", "instagram.com"]):
                continue

            headers = {'User-Agent': ua.random}
            r = requests.get(url, timeout=20, headers=headers)
            r.raise_for_status()

            if 'charset' not in r.headers.get('content-type', ''):
                result = chardet.detect(r.content)
                encoding = result['encoding']
                r.encoding = encoding if encoding else 'utf-8'

            soup = BeautifulSoup(r.content, 'html.parser')

            company_name = "Unknown Company"
            if soup.find("title"):
                raw_title = soup.find("title").text.strip()
                company_name = clean_company_name(raw_title)

            page_text = soup.get_text()
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_text)
            email = emails[0] if emails else "Not Found"

            contact_person = "Not Found"
            for keyword in ["CEO", "Founder", "Director", "Owner", "Manager"]:
                match = re.search(rf"{keyword}\s+[A-Z][a-z]+(?:\s[A-Z][a-z]+)?", page_text)
                if match:
                    contact_person = match.group()
                    break

            description = "Not Available"
            if soup.find("meta", {"name": "description"}):
                description = soup.find("meta", {"name": "description"})['content']
            elif soup.find("p"):
                description = soup.find("p").get_text().strip()

            if company_name == "Unknown Company" or email == "Not Found" or not is_valid_company_name(company_name):
                continue

            linkedin_query = f"{company_name} {location} site:linkedin.com/in"
            linkedin_url = "Not Found"
            try:
                linkedin_results = list(search(linkedin_query, stop=1))
                if linkedin_results:
                    linkedin_url = linkedin_results[0]
            except:
                pass

            result_list.append({
                "Company Name": company_name,
                "Website": url,
                "Email": email,
                "Contact Person": contact_person,
                "Industry": industry.title(),
                "Location": location.title(),
                "LinkedIn": linkedin_url,
                "Description": description
            })

            if len(result_list) >= 10:
                break

            time.sleep(random.uniform(2, 4))

        except requests.exceptions.HTTPError as http_err:
            print(f"❌ Skipped due to error: {http_err}")
            continue
        except Exception as e:
            print(f"❌ Skipped due to error: {e}")
            continue

        progress_bar.set((i + 1) / total)
        app.update()

    if not result_list:
        log_label.configure(text="⚠️ No data found.", text_color="red")
        return

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    global latest_file
    csv_path = os.path.join(save_dir, f"SalesLeads_{timestamp}.csv")
    xlsx_path = os.path.join(save_dir, f"SalesLeads_{timestamp}.xlsx")
    latest_file = csv_path

    df = pd.DataFrame(result_list)
    df.to_csv(csv_path, index=False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
    df.to_excel(xlsx_path, index=False)

    log_label.configure(text=f"✅ {len(result_list)} leads saved to folder.", text_color="green")
    open_button.pack()
    # folder_button.pack()

def threaded_scrape():
    threading.Thread(target=scrape_companies).start()

# GUI Layout
app = ctk.CTk()
app.title("Sales Lead Scraper (with LinkedIn & CSV/Excel)")
app.geometry("520x500")

title_label = ctk.CTkLabel(app, text="📊 Sales Process Automation - Smart Scraper", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

industry_frame = ctk.CTkFrame(app, fg_color="transparent")
industry_frame.pack(pady=(20, 10))

industry_label = ctk.CTkLabel(industry_frame, text="🔹 Industry:", font=("Arial", 14, "bold"),
                               text_color="#1E90FF", width=100, anchor="w")
industry_label.pack(side="left", padx=(0, 10))

entry_industry = ctk.CTkEntry(industry_frame, placeholder_text="e.g., IT, Pharma", width=300)
entry_industry.pack(side="left")

location_frame = ctk.CTkFrame(app, fg_color="transparent")
location_frame.pack(pady=(10, 20))

location_label = ctk.CTkLabel(location_frame, text="🔹 Location:", font=("Arial", 14, "bold"),
                               text_color="#1E90FF", width=100, anchor="w")
location_label.pack(side="left", padx=(0, 10))

entry_location = ctk.CTkEntry(location_frame, placeholder_text="e.g., Delhi, Mumbai", width=300)
entry_location.pack(side="left")

scrape_button = ctk.CTkButton(app, text="Start Scraping", command=threaded_scrape, width=200)
scrape_button.pack(pady=20)

progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.set(0)
progress_bar.pack(pady=10)

log_label = ctk.CTkLabel(app, text="", text_color="green")
log_label.pack(pady=10)

open_button = ctk.CTkButton(app, text="📂 Open CSV File", command=lambda: open_csv(latest_file))
open_button.pack(pady=5)
open_button.pack_forget()

# folder_button = ctk.CTkButton(app, text="📁 Open Folder", command=open_folder)
# folder_button.pack(pady=5)
# folder_button.pack_forget()

close_button = ctk.CTkButton(app, text="❌ Exit", command=app.destroy)
close_button.pack(pady=5)

app.mainloop()
