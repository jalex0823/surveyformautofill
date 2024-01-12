from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service

class SurveyAutoFiller:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        try:
            edge_service = Service(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=edge_service)
            print("Driver setup successful.")
        except Exception as e:
            print("Error setting up driver:", e)
    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def auto_fill_survey(self, url):
        self.setup_driver()
        try:
            self.driver.get(url)
            while True:
                links = self.driver.find_elements_by_tag_name('a')
                answer_links = [link for link in links if "answer" in link.get_attribute('href')]
                if not answer_links:
                    break

                random.choice(answer_links).click()
                self.wait_for_element(By.TAG_NAME, 'body')
        except TimeoutException:
            print("Timed out waiting for page to load.")
        finally:
            self.driver.quit()

    def run_script(self, url):
        if not url:
            messagebox.showerror("Error", "Please enter a URL.")
            return
        try:
            self.auto_fill_survey(url)
            messagebox.showinfo("Success", "Survey submitted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def paste_url(self):
        url_entry.delete(0, tk.END)
        url_entry.insert(0, root.clipboard_get())

    def delete_url(self):
        url_entry.delete(0, tk.END)

if __name__ == "__main__":
    survey_auto_filler = SurveyAutoFiller()

    root = ThemedTk(theme="equilux")
    root.title("Survey Auto-Filler")

    frame = ttk.Frame(root)
    frame.pack()

    url_label = ttk.Label(frame, text="Survey URL:")
    url_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

    url_entry = ttk.Entry(frame, width=50)
    url_entry.grid(row=1, column=0, columnspan=3, sticky="nsew")

    paste_button = ttk.Button(frame, text="Paste URL", command=survey_auto_filler.paste_url)
    paste_button.grid(row=2, column=0, sticky="nsew")

    run_button = ttk.Button(frame, text="Run Script", command=lambda: survey_auto_filler.run_script(url_entry.get()))
    run_button.grid(row=2, column=1, sticky="nsew")

    delete_button = ttk.Button(frame, text="Delete URL", command=survey_auto_filler.delete_url)
    delete_button.grid(row=2, column=2, sticky="nsew")

    root.mainloop()
