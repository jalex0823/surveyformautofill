import requests
from bs4 import BeautifulSoup
from getpass import getpass

class SurveyAutoFiller:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://myvoice-surveys.com"
        self.login_url = f"{self.base_url}/login"
        self.survey_url = f"{self.base_url}/survey"
        self.username = input("Enter your username/email: ")
        self.password = getpass("Enter your password: ")

    def login(self):
        login_data = {
            "email": self.username,
            "password": self.password,
        }

        response = self.session.post(self.login_url, data=login_data)

        if response.ok:
            print("Login successful.")
        else:
            print("Login failed. Please check your credentials.")
            response.raise_for_status()

    # Continue to the next part after confirming the success of this part.
class SurveyAutoFiller:
    # ... (previous methods remain unchanged)

    def fill_survey(self):
        survey_page = self.session.get(self.survey_url)

        if survey_page.ok:
            soup = BeautifulSoup(survey_page.content, "html.parser")
            form_data = {}

            # Extract form input fields and their values
            for input_tag in soup.find_all("input"):
                if input_tag.get("name"):
                    form_data[input_tag["name"]] = input_tag.get("value", "")

            # Submit the form data
            response = self.session.post(self.survey_url, data=form_data)

            if response.ok:
                print("Survey submitted successfully.")
            else:
                print("Failed to submit survey.")
                response.raise_for_status()
        else:
            print("Failed to access the survey page.")
            survey_page.raise_for_status()

if __name__ == "__main__":
    survey_auto_filler = SurveyAutoFiller()
    survey_auto_filler.login()
    survey_auto_filler.fill_survey()

