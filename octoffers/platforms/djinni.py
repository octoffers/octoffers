import re
from os import environ
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from octoffers.platforms.driver import Driver
from octoffers.db.schemes.djinni import db

class Djinni(Driver):

    def __init__(self, domain="djinni.co"):
        super().__init__(domain)
        self.origin = f"https://{domain}/jobs/"
        self.chrome_args = ("--headless", "--no-sandbox", "--disable-dev-shm-usage")
        try:
            self.session_cookies = [{"name": "sessionid", "value": environ["DJINNI_SESSION_ID"], "domain": ".djinni.co"}]
        except KeyError:
            print("ERROR: Cookies aren't set")
            exit(1)

    def _get_job_list(self, url):
        self.driver.get(url)
        self.driver.find_elements()
        return self.wait.until(
            lambda driver: driver.find_elements(
                By.XPATH, "//li[starts-with(@id, 'job-item-')]" 
            )
        )

    def _parse_salary(self, salary_text):
        # Extracting numeric values from a salary string
        numbers = [int(s) for s in re.findall(r"\b\d+\b", salary_text)]
        return min(numbers) if numbers else 0

    def fetch(
        self,
        role=None,
        tools=None,
        min_salary=None,
        exclusion_words: tuple = None,
        pages: int = 1,
    ):
        self._initiate_driver(*self.chrome_args)
        self.session_authorization()
        for idx in range(1, pages + 1):
            full_url = (
                f"{self.origin}?all-keywords={role}&keywords={role}&page={idx}"
                if role
                else f"{self.origin}?page={idx}"
            )
            job_list = self._get_job_list(full_url)

            print(full_url)  

            if self.driver.current_url == self.origin:
                print("Redieected to the main page")
                break

            for job_item in job_list:
                title_element = job_item.find_element(By.CSS_SELECTOR, "h3 > a")
                job_title = title_element.text
                job_link = title_element.get_attribute("href")
                job_id = job_link.split("/jobs/")[1].split("-")[0]

                description_element_id = "job-description-" + job_id
                job_description = job_item.find_element(
                    By.ID, description_element_id
                ).text

                # Retrieving salary information
                salary_element = job_item.find_elements(
                    By.CSS_SELECTOR, "span.public-salary-item"
                )
                salary_text = salary_element[0].text if salary_element else None
                salary = self._parse_salary(salary_text) if salary_text else 0

                # Checking tools, minimum wage and exception words
                matches = True  # By default, we assume that the vacancy is suitable

                print(
                    f"{job_title}\n   |- {job_id}\n   |- Salary: {salary}\n   |- {job_link}\n  |- Matches: {matches}"
                )

                if tools and not all(
                    tool.lower() in job_description.lower() for tool in tools
                ):
                    matches = False  # If no tools are found
                    print("Condition triggered tools")
                if min_salary and salary < min_salary:
                    matches = False  # If the salary is below the minimum
                    print("Condition triggered min_salary")
                if exclusion_words and any(
                    word.lower() in job_title.lower() for word in exclusion_words
                ):
                    matches = False  # If exception words are found
                    print("Condition triggered exclusion_words")
                # !IMPLEMENT THIS LATER!
                # if keywords and any(
                #     not word.lower() in job_title.lower() for word in keywords # ):
                #     matches = False  # If exception words are found
                #     print("Condition triggered keywords")

                job_exists = db.execute(
                    "SELECT 1 FROM jobs WHERE job_id = ?", (job_id,)).fetchone()

                if not job_exists:
                    try:
                        db.execute(
                            "INSERT INTO jobs(job_id, role, link, category, source, description, salary, matches) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                job_id,
                                job_title,
                                job_link,
                                "my_role",
                                "djinni",
                                job_description,
                                salary,
                                matches,
                            ),
                        )
                        db.commit()
                    except sqlite3.Error as e:
                        print(f"Data insertion error: {e}")

    def apply(self, msg: str, ai_generated_letter: bool = False):
        self._initiate_driver(*self.chrome_args)
        self.session_authorization()
        # Retrieving all matching records from a database
        job_entries = db.execute(
            "SELECT job_id, role, link, category, source, description FROM jobs WHERE matches = 1 AND cv_sent = 0"
        ).fetchall()

        for job_entry in job_entries:  # [:1]:
            job_id, role, job_link, category, source, job_description = job_entry
            print(f"{job_link:<80} Checking...")

            self.driver.get(job_link)

            try:
                apply_button = self.wait.until(
                    lambda driver: driver.find_element(
                        By.CSS_SELECTOR,
                        "button.btn.btn-primary.js-inbox-toggle-reply-form",
                    )
                )
                # Take and save a screenshot
                # self.driver.save_screenshot("screenshots/screenshot_send_cv.png")
                apply_button.click()
            except TimeoutException:
                print("Button not found or already applied")
                self.driver.save_screenshot("screenshots/screenshot_send_cv.png")
                continue

            if msg:
                cover_letter = msg
            else:
                print("ERROR: Pass cover letter to the arguments")
                exit(1)

            try:
                message_box = self.wait.until(
                    lambda driver: driver.find_element(By.ID, "message")
                )
                message_box.send_keys(cover_letter)
                submit_button = self.wait.until(
                    lambda driver: driver.find_element(By.ID, "job_apply")
                )
                submit_button.click()
            except TimeoutException:
                print("Could not send application")
                continue

            # Updating the submission status in the database
            db.execute("UPDATE jobs SET cv_sent = 1 WHERE job_id = ?", (job_id,))
            db.commit()

            print(f"Application sent for {job_link}")
