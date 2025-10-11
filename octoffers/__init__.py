from fire import Fire
from octoffers.platforms.profile import Profile
Profile(name="default")
from octoffers.platforms.djinni import Djinni
from octoffers.platforms.ziprecruiter import ZipRecruiter
from octoffers.logger import log
from sys import path
from pathlib import Path
from os import environ

class Octoffers:
    def __init__(self, profile: str = None):
        self.djinni = Djinni()
        self.ziprecruiter = ZipRecruiter()
        self.profile = Profile()
        try:
            from octoffers_private.platforms.indeed import Indeed
            self.indeed = Indeed(profile=profile)
        except ModuleNotFoundError:
            log.info("Indeed Driver isn't installed")

    def manual_authorization(self):
        self.djinni.manual_authorization()

def main():
    Fire(Octoffers)
