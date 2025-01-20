from octoffers.logger import log
from selenium.webdriver.common.by import By
from octoffers.platforms.driver import Driver
from octoffers.db.schemes.ziprecruiter import db
from os import environ 
from sys import exit

class ZipRecruiter(Driver):

    def __init__(self, domain="ziprecruiter.com"):
        super().__init__(domain)
        self.origin = f"https://{domain}/jobs-search" 
        self.chrome_args = ("--no-sandbox", "--disable-dev-shm-usage")
        try:
            self.session_cookies = [{
                "name": "ziprecruiter_session",
                "value": environ["ZIPRECRUITER_SESSION"],
                "domain": ".ziprecruiter.com"
            }]
        except KeyError:
            log.error("Session Cookies aren't set in your environment variables")
            exit(1)

    def fetch(self, role: str, location: str, pages: int = 1):
        self._initiate_driver(*self.chrome_args)
        self.session_authorization()
        for idx in range(1, pages):
            url = f"{self.origin}?search={role}&location={location}&page={idx}" 
            self.driver.get(url)
            breakpoint()
