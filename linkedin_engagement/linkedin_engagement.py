from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, re, sys, traceback
import os

# Import credentials
from creds import *

# Initialize variables
start_time = time.time()
output_file_path = 'postOutput.txt'
input_file_path = os.path.join(os.getcwd(), 'postInput.txt')


# Set Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=chrome_options)

# Function to login to LinkedIn
def linkedin_login():
    driver.get('https://www.linkedin.com')
    time.sleep(5)
    print("Linkedin Logging In...")
    username_input = driver.find_element(By.ID, "session_key")
    username_input.send_keys(lnkdn_username)
    password_input = driver.find_element(By.ID, "session_password")
    password_input.send_keys(lnkdn_pass)
    login_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
    login_button.click()
    time.sleep(6)
    print("Linkedin Login Successful")

# Read post links from the file
with open('linkedin_engagement\postInput.txt', 'r') as file:
    post_links = file.readlines()

# Login to LinkedIn
linkedin_login()

# Process each post link
for post_link in post_links:
    post_link = post_link.strip()
    driver.get(post_link)
    time.sleep(6)

    comment_box = driver.find_element(By.CLASS_NAME, "comments-comments-list")
    while True:
        try:
            load_more_comments = driver.find_element(By.CLASS_NAME, 'comments-comments-list__show-previous-container')
            button_element = load_more_comments.find_element(By.TAG_NAME, "button")
            button_element.click()
            time.sleep(4)

            try:
                load_more_replies = driver.find_elements(By.CLASS_NAME, "button.show-prev-replies.t-12.t-black.t-normal.hoverable-link-text")
                for element in load_more_replies:
                    element.click()
                    driver.implicitly_wait(3)
            except:
                pass

        except Exception as e:
            print(e)
            traceback_details = traceback.extract_tb(sys.exc_info()[2])
            for trace in traceback_details:
                filename, lineno, function, line = trace
                print(f"File: {filename}, Line: {lineno}, in {function}\n\t{line}")
            break

    # Extract LinkedIn profile URLs from the HTML
    html_text = comment_box.get_attribute('innerHTML')
    linkedin_urls = re.findall(r'/in/[^\s]+', html_text)
    linkedin_urls = list(set(linkedin_urls))

    # Write output to file
    with open(output_file_path, 'w') as file:
        for item in linkedin_urls:
            file.write("https://www.linkedin.com" + item + "\n")

# Close the driver
driver.quit()
print("Job Finished !!!")
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
