from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from chrome_version import get_chrome_version
from os import getenv, name as osname
from pathlib import Path
import undetected_chromedriver as uc
from octoffers.logger import log


load_dotenv()

class Driver:
    def __init__(self, domain: str = None):
        self.domain = domain
        self.session_cookies = list()
        self.octoffers_path = Path.home() / "Octoffers" if osname == "nt" else Path.home() / ".config/octoffers"
        self.profile_name = "default"
        self.profile_path = self.octoffers_path / "profiles" / self.profile_name

    def _initiate_driver(self, *argv):
        # Create octoffers directory if it doesn't exist
        self.init_octoffers_path()
        
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={self.profile_path}")
        log.info(f"Profile {self.profile_name} has been loaded")
        for arg in argv:
            options.add_argument(str(arg))
        driver_path = ChromeDriverManager(get_chrome_version()).install()
        self.driver = webdriver.Chrome(options=options) 

        self.wait = WebDriverWait(self.driver, 5)

    def session_authorization(self):
        self.driver.get(f"https://{self.domain}")

        # Adding an explicit wait to ensure the page has loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        for cookie in self.session_cookies:
            self.driver.add_cookie(cookie)

        # Reloading the page to apply cookies
        self.driver.refresh()
        log.info("Session cookies are set")
    
    def init_octoffers_path(self):
        if not self.octoffers_path.exists():
            self.octoffers_path.mkdir(parents=True, exist_ok=True)
            log.info(f"Created Octoffers directory at {self.octoffers_path}")
