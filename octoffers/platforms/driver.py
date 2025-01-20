from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from os import getenv, name as osname
from pathlib import Path
import undetected_chromedriver as uc


load_dotenv()

class Driver:
    def __init__(self, domain: str = None):
        self.domain = domain
        self.session_cookies = list()
        self.octoffers_path = Path.home() / "Octoffers" if osname == "nt" else Path.home() / ".config/octoffers"
        self.profile_name = "default"
        self.profile_path = self.octoffers_path / "profiles" / self.profile_name

    def _initiate_driver(self, *argv):
        options = webdriver.ChromeOptions()
        for arg in argv:
            options.add_argument(str(arg))
        
        self.driver = uc.Chrome(options=options)

        #self.wait = WebDriverWait(self.driver, 5)

    def session_authorization(self):
        self.driver.get(f"https://{self.domain}")

        # Adding an explicit wait to ensure the page has loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        for cookie in self.session_cookies:
            self.driver.add_cookie(cookie)

        # Reloading the page to apply cookies
        # self.driver.refresh()
