import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
import random
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk, ThemedStyle
import datetime
from tkinter import messagebox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def check_submission(driver):
    # Wait for the success element or text to be present on the page
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 'element_or_text_indicating_success')))
        print("Survey submitted successfully.")
        return True
    except:
        print("Failed to submit the survey.")
        return False

def auto_fill_survey(url):
    # Create a new instance of the Edge driver
    driver = webdriver.Edge(service=Service('C:/Temp/surveyformautofill/msedgedriver.exe'))  # Replace with the path to your Edge driver

    # Go to the page that we want to scrape
    driver.get(url)

    try:
        # Wait for the form to be present on the page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
        # Locate the form in the HTML
        form = driver.find_element_by_tag_name('form')
    except:
        print("Failed to find form. Page source:")
        print(driver.page_source)
        return

    # Check if the form exists
    if form is None:
        print("No form found on the page.")
        return

    # Prepare form data for submission
    for input_field in form.find_elements_by_tag_name('input'):
        input_type = input_field.get_attribute('type')
        input_name = input_field.get_attribute('name')

        if input_type in ['radio', 'checkbox']:
            # Handle multiple-choice questions
            options = form.find_elements_by_xpath(f'//input[@name="{input_name}"]')
            random.choice(options).click()
        elif input_type in ['text', 'email', 'password', 'number']:
            # Handle text input fields
            input_field.send_keys('test')  # Replace with appropriate value
        elif input_type == 'file':
            # Handle file input fields
            input_field.send_keys('/path/to/your/file')  # Replace with appropriate file path
        elif input_type == 'date':
            # Handle date input fields
            input_field.send_keys(datetime.date.today().isoformat())  # Replace with appropriate date

    for select in form.find_elements_by_tag_name('select'):
        select_name = select.get_attribute('name')
        options = select.find_elements_by_tag_name('option')
        random.choice(options).click()

    # Submit the form
    form.submit()

    # Check if the form was submitted successfully
    if check_submission(driver):
        messagebox.showinfo("Success", "Survey submitted successfully.")
    else:
        messagebox.showerror("Error", "Failed to submit the survey.")

    # Close the browser
    driver.quit()

def run_script():
    url = url_entry.get()
    try:
        auto_fill_survey(url)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def paste_url():
    url_entry.delete(0, tk.END)  # Clear the entry field
    url_entry.insert(0, root.clipboard_get())  # Paste from clipboard

def delete_url():
    url_entry.delete(0, tk.END)  # Clear the entry field

# Create the main window
root = ThemedTk(theme="black")  # Use the "black" theme for a dark theme
root.configure(bg='black')  # Set the background color of the root window to black
root.title("Survey Auto-Filler")

# Set the geometry of the root window (width x height)
root.geometry("310x100")  # Set the width to 800 pixels and the height to 600 pixels

# Create a themed style
style = ThemedStyle(root)

# Set the theme to 'yaru' (or any other modern theme)
style.set_theme("yaru")

# Survey URL input
url_label = ttk.Label(root, text="Survey URL:")
url_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

url_entry = ttk.Entry(root, width=50)  # Set the width to 50
url_entry.grid(row=1, column=0, columnspan=3, sticky="nsew")

# Paste button
paste_button = ttk.Button(root, text="Paste URL", command=paste_url)
paste_button.grid(row=2, column=0, sticky="nsew")

# Delete button
delete_button = ttk.Button(root, text="Delete URL", command=delete_url)
delete_button.grid(row=2, column=1, sticky="nsew")

# Run button
run_button = ttk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=2, column=2, sticky="nsew")

root.mainloop()