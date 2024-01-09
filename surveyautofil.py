import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import random
import requests

def auto_fill_survey_multiple_choice(url):
    # Fetch the survey form
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the form in the HTML
    form = soup.find('form')

    # Check if the form exists
    if form is None:
        print("No form found on the page.")
        return

    # Locate all the input fields in the form
    inputs = form.find_all('input')
    selects = form.find_all('select')

    # Prepare form data for submission
    form_data = {}

    for input_field in inputs:
        input_type = input_field.get('type')
        input_name = input_field.get('name')

        if input_type in ['radio', 'checkbox']:
            # Handle multiple-choice questions
            if input_name not in form_data:
                options = [option.get('value') for option in form.find_all('input', {'name': input_name})]
                form_data[input_name] = random.choice(options)
        elif input_type in ['text', 'email', 'password', 'number']:
            # Handle text input fields
            form_data[input_name] = 'test'  # Replace with appropriate value

    for select in selects:
        select_name = select.get('name')
        options = [option.get('value') for option in select.find_all('option')]
        form_data[select_name] = random.choice(options)

    # Submit the form
    response = requests.post(url, data=form_data)

    # Check if the form was submitted successfully
    if response.status_code == 200:
        print("Survey submitted successfully.")
    else:
        print("Failed to submit the survey.")

def run_script():
    url = url_entry.get()
    try:
        auto_fill_survey_multiple_choice(url)
        messagebox.showinfo("Success", "Survey submitted successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Survey Auto-Filler")

# Survey URL input
url_label = tk.Label(root, text="Survey URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

# Run button
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack()

root.mainloop()