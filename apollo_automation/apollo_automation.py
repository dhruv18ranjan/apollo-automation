import os
import requests
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import re  # Import regular expressions module

# Global variable to store error content
error_content = ""

def enrich_people(lurl, api_key):
    url = "https://api.apollo.io/v1/people/match"
    data = {
        "linkedin_url": lurl,
        "reveal_personal_emails": True,
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    response = requests.request("POST", url, headers=headers, json=data)
    return response.json()

def enrich_org(primary_domain, api_key):
    url = "https://api.apollo.io/v1/organizations/enrich"
    querystring = {
        "domain": primary_domain
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def search_contact(lurl, response_data, api_key, list_name):
    url = "https://api.apollo.io/v1/contacts/search"
    data = {
        "q_keywords": response_data["person"]["email"],
        "sort_by_field": "contact_last_activity_date",
        "sort_ascending": False,
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    response = requests.request("POST", url, headers=headers, json=data)
    response = response.json()
    if response["contacts"] == []:
        create_contact(lurl, response_data, api_key, list_name)
    elif lurl == response["contacts"][0]["linkedin_url"]:
        update_contact(response_data, response["contacts"][0]["id"], api_key, list_name)
    else:
        create_contact(lurl, response_data, api_key, list_name)

def update_contact(response_data, contact_id, api_key, list_name):
    url = "https://api.apollo.io/v1/contacts/" + contact_id
    response_data["label_names"] = [list_name]
    data = {
        "first_name": response_data["person"]["first_name"],
        "last_name": response_data["person"]["last_name"],
        "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
        "title": response_data["person"]["title"],
        "email": response_data["person"]["email"],
        "website_url": response_data["person"]["organization"]["primary_domain"],
        "label_names": response_data["label_names"]
    }
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    response = requests.request("PUT", url, headers=headers, json=data)

def create_contact(lurl, response_data, api_key, list_name):
    url = "https://api.apollo.io/v1/contacts"
    response_data["label_names"] = [list_name]
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    try:
        primary_domain = response_data["person"]["organization"]["primary_domain"]
        if primary_domain != "None":
            org_data = enrich_org(primary_domain, api_key)
    except Exception as e:
        data = {
            "first_name": response_data["person"]["first_name"],
            "last_name": response_data["person"]["last_name"],
            "title": response_data["person"]["title"],
            "email": response_data["person"]["email"],
            "label_names": response_data["label_names"]
        }
        response = requests.request("POST", url, headers=headers, json=data)
        return

    data = {
        "first_name": response_data["person"]["first_name"],
        "last_name": response_data["person"]["last_name"],
        "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
        "title": response_data["person"]["title"],
        "email": response_data["person"]["email"],
        "website_url": response_data["person"]["organization"]["primary_domain"],
        "label_names": response_data["label_names"]
    }

    if "account_id" in org_data["organization"]:
        data["account_id"] = org_data["organization"]["account_id"]
    elif "id" in org_data["organization"]:
        data["account_id"] = org_data["organization"]["id"]

    response = requests.request("POST", url, headers=headers, json=data)

def check_api(api_key):
    url = "https://api.apollo.io/v1/auth/health"
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    response = requests.request("GET", url, headers=headers)
    return response.text

def get_rate_limits(api_key):
    url = "https://api.apollo.io/v1/people/match"
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    data = {
        "linkedin_url": "https://www.linkedin.com/in/sample-profile",
        "reveal_personal_emails": True
    }
    response = requests.request("POST", url, headers=headers, json=data)

    rate_limit_info = {
        "minutely_limit": response.headers.get("x-rate-limit-minute"),
        "minutely_remaining": response.headers.get("x-minute-requests-left"),
        "hourly_limit": response.headers.get("x-rate-limit-hourly"),
        "hourly_remaining": response.headers.get("x-hourly-requests-left"),
        "daily_limit": response.headers.get("x-rate-limit-24-hour"),
        "daily_remaining": response.headers.get("x-24-hour-requests-left")
    }

    return rate_limit_info

def wait_for_hourly_limit(log):
    log.insert(tk.END, "Hourly limit reached. Waiting for 1 hour before continuing...\n")
    for remaining in range(3600, 0, -1):
        log.insert(tk.END, f"Waiting for {remaining // 60} minutes and {remaining % 60} seconds...\n")
        log.yview(tk.END)
        time.sleep(1)
    log.insert(tk.END, "Continuing...\n")
    log.yview(tk.END)

def process_urls(api_key, list_name, log, input_file_path):
    log.insert(tk.END, "Started\n")
    rate_limits = get_rate_limits(api_key)
    log.insert(tk.END, f"Rate Limits:\nMinutely data uploading remaining: {rate_limits['minutely_remaining']}\nHourly data uploading remaining: {rate_limits['hourly_remaining']}\nDaily data uploading remaining: {rate_limits['daily_remaining']}\n")
    log.yview(tk.END)

    errors = []

    # Ask the user if they want to continue
    proceed = messagebox.askyesno("Continue?", "Do you want to continue?")

    if not proceed:
        log.insert(tk.END, "Operation cancelled.\n")
        log.yview(tk.END)
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        log.insert(tk.END, f"File not found: {input_file_path}\n")
        log.yview(tk.END)
        return
    except Exception as e:
        log.insert(tk.END, f"An error occurred while opening the file: {e}\n")
        log.yview(tk.END)
        return

    lines = [line.strip() for line in lines]

    total_lines = len(lines)
    batch_size = 200
    for start in range(0, total_lines, batch_size):
        end = min(start + batch_size, total_lines)
        for idx, line in enumerate(lines[start:end], start=start):
            try:
                response_data = enrich_people(line, api_key)
                search_contact(line, response_data, api_key, list_name)
                log.insert(tk.END, f"Processed line {idx+1} of {total_lines}.\n")
                log.yview(tk.END)
            except Exception as e:
                log.insert(tk.END, f"Error processing line {idx+1}: {e}\n")
                log.yview(tk.END)
                errors.append(f"{line} {str(e)}")
        
        if end < total_lines:
            wait_for_hourly_limit(log)

    log.insert(tk.END, "All URLs have been processed.\n")
    log.yview(tk.END)

    # Save errors globally
    global error_content
    error_content = save_errors(errors)

    # Enable download button
    download_button.config(state=tk.NORMAL)

    return errors

def save_errors(errors):
    # Regular expression to extract URLs
    url_pattern = r"(https?://[^\s]+)"
    error_urls = []
    for error in errors:
        match = re.search(url_pattern, error)
        if match:
            error_urls.append(match.group(0))
    error_content = "\n".join(error_urls)
    return error_content

def browse_file(file_entry):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def download_errors():
    global error_content
    if not error_content:
        messagebox.showinfo("No Errors", "No errors to download.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(error_content)
            messagebox.showinfo("Download Complete", f"Error file saved successfully: {file_path}")
        except Exception as e:
            messagebox.showerror("Error Saving File", f"An error occurred while saving error file: {e}")

def start_processing(api_key_entry, list_name_entry, log, file_entry):
    api_key = api_key_entry.get().strip()
    list_name = list_name_entry.get().strip()
    input_file_path = file_entry.get().strip()

    if not api_key or not list_name or not input_file_path:
        messagebox.showerror("Input Error", "API key, list name, and file path are required.")
        return

    errors = process_urls(api_key, list_name, log, input_file_path)
    return errors

def main():
    app = tk.Tk()
    app.title("Apollo Automation Tool")

    tk.Label(app, text="API Key:").grid(row=0, column=0, padx=10, pady=10)
    api_key_entry = tk.Entry(app, width=40)
    api_key_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(app, text="List Name:").grid(row=1, column=0, padx=10, pady=10)
    list_name_entry = tk.Entry(app, width=40)
    list_name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(app, text="Input File:").grid(row=2, column=0, padx=10, pady=10)
    file_entry = tk.Entry(app, width=40)
    file_entry.grid(row=2, column=1, padx=10, pady=10)

    browse_button = tk.Button(app, text="Browse", command=lambda: browse_file(file_entry))
    browse_button.grid(row=2, column=2, padx=10, pady=10)

    log = scrolledtext.ScrolledText(app, width=80, height=20, wrap=tk.WORD)
    log.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    start_button = tk.Button(app, text="Start Processing", command=lambda: start_processing(api_key_entry, list_name_entry, log, file_entry))
    start_button.grid(row=4, column=0, columnspan=3, pady=10)

    global download_button
    download_button = tk.Button(app, text="Download Errors", state=tk.DISABLED, command=download_errors)
    download_button.grid(row=5, column=0, columnspan=3, pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()
