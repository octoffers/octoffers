from octoffers.logger import log
from selenium.webdriver.common.by import By
from octoffers.platforms.driver import Driver
from octoffers.db.schemes.ziprecruiter import db

class ZipRecruiter(Driver):

    def __init___(self, domain="ziprecruiter.com"):
        super().__init__(domain)
