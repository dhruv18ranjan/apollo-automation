import subprocess
import os
import tkinter as tk
from tkinter import messagebox

def run_script(script_path):
    """Run a Python script located at script_path."""
    try:
        subprocess.run(['python', script_path], check=True)
        messagebox.showinfo("Success", f"{os.path.basename(script_path)} ran successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running the script: {e}")

def on_select(choice):
    if choice == '1':
        script_path = os.path.join('apollo_automation', 'apollo_automation.py')
    elif choice == '2':
        script_path = os.path.join('linkedin_engagement', 'linkedin_engagement.py')
    elif choice == '3':
        script_path = os.path.join('url_converter', 'url_converter.py')
    else:
        messagebox.showerror("Invalid choice", "Invalid choice. Please select 1, 2, or 3.")
        return

    if os.path.exists(script_path):
        run_script(script_path)
    else:
        messagebox.showerror("Error", f"Script not found: {script_path}")

def main():
    app = tk.Tk()
    app.title("Script Runner")

    # Calculate the screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Set the width and height of the window
    window_width = int(screen_width * 0.7)
    window_height = int(screen_height * 0.7)

    # Calculate the position of the window
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the geometry of the window
    app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    title_label = tk.Label(app, text="Script Runner", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    instruction_label = tk.Label(app, text="Select the script to run:")
    instruction_label.pack()

    button_frame = tk.Frame(app)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Apollo Automation", command=lambda: on_select('1'), width=20, relief=tk.GROOVE, bd=2).pack(pady=5)
    tk.Button(button_frame, text="LinkedIn Engagement", command=lambda: on_select('2'), width=20, relief=tk.GROOVE, bd=2).pack(pady=5)
    tk.Button(button_frame, text="URL Converter", command=lambda: on_select('3'), width=20, relief=tk.GROOVE, bd=2).pack(pady=5)

    app.mainloop()

if __name__ == "__main__":
    main()

