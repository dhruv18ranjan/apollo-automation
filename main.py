import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True)
        print(f"{script_name} ran successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")

if __name__ == "__main__":
    print("Choose an option to run:")
    print("1. Run script for Apollo Automation Tool")
    print("2. Run script for Linkedin Long Url converter")
    print("3. Run script for linkedin Posts Engagement Scrapper")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ").strip()

    if choice == '1':
        run_script('apollo_new.py')
    elif choice == '2':
        run_script('ln_people.py')
    elif choice == '3':
        run_script('ln_post_comments.py')
    elif choice == '4':
        print("Exiting.")
    else:
        print("Invalid choice. Exiting.")
