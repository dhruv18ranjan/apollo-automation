from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from creds import *

import time, traceback,sys

start_time = time.time()

file_path = 'shortUrls.txt'
output_file_path = 'longUrls.txt'
error_file_path = 'urlError.txt'
temp_store=""

while(True):
    try:
        # Set Chrome options for headless browsing
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--disable-gpu')
#        chrome_options.add_argument(f'--load-extension={extension_path}')
        # Initialize Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to LinkedIn
        driver.get('https://www.linkedin.com')
        time.sleep(5)
        print("Linkedin Logging In...")

        username_input =  driver.find_element("id", "session_key")
        username_input.send_keys(lnkdn_username)

        password_input = driver.find_element("id", "session_password")
        password_input.send_keys(lnkdn_pass)

        login_button = driver.find_element('xpath', '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
        login_button.click()

        time.sleep(10)
        print("Linkedin Login Successful")


        # Navigate to a different website in the new tab
        list_of_url = []
        out_list_of_url = []
        list_of_items = []
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        # Open the file in read mode ('r')
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                list_of_url.append(line)



        try:
            print("Start Saving Contacts on Apollo")
            
            for i in range(0, len(list_of_url)):
                if not (list_of_url[i]).strip() in out_list_of_url:
                    print(str(i+1) +" "+ list_of_url[i])

                    driver.get(list_of_url[i])
                    time.sleep(3)

                    # Get the current URL of the page
                    current_url = driver.current_url

                    with open(output_file_path, 'a') as file:
                    # Write each item to a new line in the file
                        file.write("\n")
                        file.write(current_url)



        except Exception as e:
            print("Error:" + str(e))            
            continue
    except Exception as e:
        print("Error:" + str(e))
        print("Trying Again")

        traceback_details = traceback.extract_tb(sys.exc_info()[2])
        for trace in traceback_details:
            filename, lineno, function, line = trace
            print(f"File: {filename}, Line: {lineno}, in {function}\n\t{line}")


        with open(error_file_path, 'a') as file:
            file.write(temp_store + "\n")
            
        continue


    print("Job Finished !!!")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    # Close the driver
    driver.quit()
    break
