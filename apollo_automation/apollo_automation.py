# import os
# import requests
# import time

# def enrich_people(lurl, api_key):
#     url = "https://api.apollo.io/v1/people/match"

#     data = {
#         "linkedin_url": lurl,
#         "reveal_personal_emails": True,
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("POST", url, headers=headers, json=data)
#     return response.json()

# def enrich_org(primary_domain, api_key):
#     url = "https://api.apollo.io/v1/organizations/enrich"

#     querystring = {
#         "domain": primary_domain
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("GET", url, headers=headers, params=querystring)
#     return response.json()

# def search_contact(lurl, response_data, api_key, list_name):
#     url = "https://api.apollo.io/v1/contacts/search"

#     data = {
#         "q_keywords": response_data["person"]["email"],
#         "sort_by_field": "contact_last_activity_date",
#         "sort_ascending": False,
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("POST", url, headers=headers, json=data)
#     response = response.json()

#     if response["contacts"] == []:
#         create_contact(lurl, response_data, api_key, list_name)
#     elif lurl == response["contacts"][0]["linkedin_url"]:
#         update_contact(response_data, response["contacts"][0]["id"], api_key, list_name)
#     else:
#         create_contact(lurl, response_data, api_key, list_name)

# def update_contact(response_data, contact_id, api_key, list_name):
#     url = "https://api.apollo.io/v1/contacts/" + contact_id

#     response_data["label_names"] = [list_name]

#     data = {
#         "first_name": response_data["person"]["first_name"],
#         "last_name": response_data["person"]["last_name"],
#         "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
#         "title": response_data["person"]["title"],
#         "email": response_data["person"]["email"],
#         "website_url": response_data["person"]["organization"]["primary_domain"],
#         "label_names": response_data["label_names"]
#     }

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("PUT", url, headers=headers, json=data)

# def create_contact(lurl, response_data, api_key, list_name):
#     url = "https://api.apollo.io/v1/contacts"

#     response_data["label_names"] = [list_name]

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     try:
#         primary_domain = response_data["person"]["organization"]["primary_domain"]
#         if primary_domain != "None":
#             print(response_data["person"]["organization"]["primary_domain"], "primary")
#             org_data = enrich_org(primary_domain, api_key)
#     except Exception as e:
#         data = {
#             "first_name": response_data["person"]["first_name"],
#             "last_name": response_data["person"]["last_name"],
#             "title": response_data["person"]["title"],
#             "email": response_data["person"]["email"],
#             "label_names": response_data["label_names"]
#         }
#         response = requests.request("POST", url, headers=headers, json=data)
#         return

#     data = {
#         "first_name": response_data["person"]["first_name"],
#         "last_name": response_data["person"]["last_name"],
#         "organization_name": response_data["person"]["employment_history"][0]["organization_name"],
#         "title": response_data["person"]["title"],
#         "email": response_data["person"]["email"],
#         "website_url": response_data["person"]["organization"]["primary_domain"],
#         "label_names": response_data["label_names"]
#     }

#     if "account_id" in org_data["organization"]:
#         data["account_id"] = org_data["organization"]["account_id"]
#     elif "id" in org_data["organization"]:
#         data["account_id"] = org_data["organization"]["id"]

#     response = requests.request("POST", url, headers=headers, json=data)

# def check_api(api_key):
#     url = "https://api.apollo.io/v1/auth/health"

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     response = requests.request("GET", url, headers=headers)
#     print(response.text)

# def get_rate_limits(api_key):
#     url = "https://api.apollo.io/v1/people/match"

#     headers = {
#         'Cache-Control': 'no-cache',
#         'Content-Type': 'application/json',
#         'X-Api-Key': api_key
#     }

#     data = {
#         "linkedin_url": "https://www.linkedin.com/in/sample-profile",
#         "reveal_personal_emails": True
#     }

#     response = requests.request("POST", url, headers=headers, json=data)

#     rate_limit_info = {
#         "minutely_limit": response.headers.get("x-rate-limit-minute"),
#         "minutely_remaining": response.headers.get("x-minute-requests-left"),
#         "hourly_limit": response.headers.get("x-rate-limit-hourly"),
#         "hourly_remaining": response.headers.get("x-hourly-requests-left"),
#         "daily_limit": response.headers.get("x-rate-limit-24-hour"),
#         "daily_remaining": response.headers.get("x-24-hour-requests-left")
#     }

#     return rate_limit_info

# def wait_for_hourly_limit():
#     print("Hourly limit reached. Waiting for 1 hour before continuing...")
#     for remaining in range(3600, 0, -1):
#         print(f"Waiting for {remaining // 60} minutes and {remaining % 60} seconds...", end='\r')
#         time.sleep(1)
#     print("Continuing...                          ")

# if __name__ == "__main__":
#     # Ask the user for API key and list name
#     api_key = input("Enter your API key: ")
#     list_name = input("Enter the list name: ")

#     print("Started")

#     # Get and display rate limit information
#     rate_limits = get_rate_limits(api_key)
#     print("Rate Limits:")
#     print(f"Minutely data uploading remaining: {rate_limits['minutely_remaining']}")
#     print(f"Hourly data uploading remaining: {rate_limits['hourly_remaining']}")
#     print(f"Daily data uploading remaining: {rate_limits['daily_remaining']}")

#     # Ask the user if they want to continue
#     proceed = input("Do you want to continue? (yes/no): ").strip().lower()

#     if proceed != 'yes':
#         print("Operation cancelled.")
#         exit()

#     # Define the path to the input file
#     input_file_path = os.path.join('apollo_automation', 'apolloInput.txt')

#     try:
#         with open(input_file_path, 'r', encoding='utf-8') as file:
#             lines = file.readlines()
#     except FileNotFoundError:
#         print(f"File not found: {input_file_path}")
#         exit()
#     except Exception as e:
#         print(f"An error occurred while opening the file: {e}")
#         exit()

#     lines = [line.strip() for line in lines]

#     total_lines = len(lines)
#     batch_size = 200
#     for start in range(0, total_lines, batch_size):
#         end = min(start + batch_size, total_lines)
#         for idx, line in enumerate(lines[start:end], start=start):
#             try:
#                 response_data = enrich_people(line, api_key)
#                 search_contact(line, response_data, api_key, list_name)
#                 print(f"Processed line {idx+1} of {total_lines}.")
#             except Exception as e:
#                 print(f"Error processing line {idx+1}: {e}")
#                 with open('apolloError.txt', 'a', encoding='utf-8') as error_file:
#                     error_file.write(f"{line}\n")
        
#         if end < total_lines:
#             wait_for_hourly_limit()

#     print("All URLs have been processed.")





import os
import requests
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext

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

def process_urls(api_key, list_name, log):
    log.insert(tk.END, "Started\n")
    rate_limits = get_rate_limits(api_key)
    log.insert(tk.END, f"Rate Limits:\nMinutely data uploading remaining: {rate_limits['minutely_remaining']}\nHourly data uploading remaining: {rate_limits['hourly_remaining']}\nDaily data uploading remaining: {rate_limits['daily_remaining']}\n")
    log.yview(tk.END)

    # Ask the user if they want to continue
    proceed = messagebox.askyesno("Continue?", "Do you want to continue?")

    if not proceed:
        log.insert(tk.END, "Operation cancelled.\n")
        log.yview(tk.END)
        return

    input_file_path = os.path.join('apollo_automation', 'apolloInput.txt')
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
                apollo_error=os.path.join('apollo_automation', 'apolloError.txt')
                with open(apollo_error, 'a', encoding='utf-8') as error_file:
                    error_file.write(f"{line}\n")
        
        if end < total_lines:
            wait_for_hourly_limit(log)

    log.insert(tk.END, "All URLs have been processed.\n")
    log.yview(tk.END)

def start_processing(api_key_entry, list_name_entry, log):
    api_key = api_key_entry.get().strip()
    list_name = list_name_entry.get().strip()

    if not api_key or not list_name:
        messagebox.showerror("Input Error", "API key and list name are required.")
        return

    process_urls(api_key, list_name, log)

def main():
    app = tk.Tk()
    app.title("Apollo Automation Tool")

    tk.Label(app, text="API Key:").grid(row=0, column=0, padx=10, pady=10)
    api_key_entry = tk.Entry(app, width=40)
    api_key_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(app, text="List Name:").grid(row=1, column=0, padx=10, pady=10)
    list_name_entry = tk.Entry(app, width=40)
    list_name_entry.grid(row=1, column=1, padx=10, pady=10)

    log = scrolledtext.ScrolledText(app, width=80, height=20, wrap=tk.WORD)
    log.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    start_button = tk.Button(app, text="Start Processing", command=lambda: start_processing(api_key_entry, list_name_entry, log))
    start_button.grid(row=3, column=0, columnspan=2, pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()

