from octoffers.logger import log
from selenium.webdriver.common.by import By
from octoffers.platforms.driver import Driver
from octoffers.db.schemes.ziprecruiter import db
from os import environ
from sys import exit
from sqlite3 import IntegrityError
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException

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

    def _authenticate(self):
        self._initiate_driver(*self.chrome_args)

        # FIXME: Currently works only with default profile
        for cookie in self.driver.get_cookies():
            if cookie["name"] == "ziprecruiter_session":
                if cookie["value"] != self.session_cookies["value"]:
                    self.session_authorization()

    def fetch(self, role: str, location: str, pages: int = 1):
        self._authenticate()

        for idx in range(1, pages+1):
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

                # FIXME: Not 100% accurate sometimes labels easy_apply falsely, idk why
                try:
                    self.wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, "[aria-label^='1-Click']"))
                    easy_apply = True
                except TimeoutException:
                    easy_apply = False

                try:
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
                    log.info(f"Committing job posting to the database: {job_url}")
                except IntegrityError as e:
                    log.error(f"Couldn't save job posting: {e}")

    # FIXME: This will apply to all available jobs with an easy apply option in the database. While not ideal, it is sufficient for most users.
    def apply(self):
        self._authenticate()
        links = db.execute("SELECT link FROM jobs WHERE applicable = TRUE AND easy_apply = TRUE").fetchall()
        for url in links:
            self.driver.get(url[0])
            buttons = self.wait.until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, "[aria-label^='1-Click']")
            )
            try:
                for button in buttons:
                    button.click()
            except:
                pass
            db.execute("UPDATE jobs SET applicable = FALSE WHERE link = ?", (url[0],))
            db.commit()
            log.info(f"Attempt to apply for the job: {url}")
