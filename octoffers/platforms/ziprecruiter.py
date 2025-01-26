from octoffers.logger import log
from selenium.webdriver.common.by import By
from octoffers.platforms.driver import Driver
from octoffers.db.schemes.ziprecruiter import db
from os import environ 
from sys import exit
from ipdb import pm
from sqlite3 import IntegrityError

class ZipRecruiter(Driver):

    def __init__(self, domain="ziprecruiter.com"):
        super().__init__(domain)
        self.origin = f"https://{domain}/jobs-search" 
        self.chrome_args = ("--disable-dev-shm-usage",)
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

        # FIXME: Currently works only with default profile
        for cookie in self.driver.get_cookies():
            if cookie["name"] == "ziprecruiter_session":
                if cookie["value"] != self.session_cookies["value"]:
                    self.session_authorization()

        for idx in range(1, pages):
            url = f"{self.origin}?search={role}&location={location}&page={idx}"
            self.driver.get(url)
            posts = self.wait.until(
                lambda driver: driver.find_elements(By.CLASS_NAME, "job_result_two_pane")
            )
            for job in posts:
                job.find_element(By.TAG_NAME, "h2").click()

                titles = self.wait.until(
                    lambda driver: driver.find_elements(By.TAG_NAME, "h1")
                )
                job_description = self.wait.until(
                    lambda driver: driver.find_element(
                        By.CSS_SELECTOR, ".text-primary.whitespace-pre-line.break-words"
                    ).text
                )

                job_url = self.driver.current_url

                try:
                    self.driver.find_element(By.CSS_SELECTOR, "[aria-label^='1-Click']")
                    easy_apply = True
                except:
                    easy_apply = False

                try:
                    log.info(f"Commiting job posting to the database: {job_url}")
                    db.execute("""
                        INSERT INTO jobs(
                            link,
                            role,
                            description,
                            easy_apply
                        ) VALUES (?,?,?,?)""", 
                        (
                        job_url,
                        "".join([title.text for title in titles]),
                        job_description,
                        easy_apply
                        )
                    )
                    db.commit()
                except IntegrityError as e:
                    log.error(f"Couldn't insert job posting: {e}")
