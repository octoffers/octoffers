from fire import Fire
from octoffers.platforms.djinni import Djinni
from octoffers.platforms.profile import Profile
from sys import path
from pathlib import Path
from os import environ

class Octoffers:
    def __init__(self, profile: str = None):
        self.djinni = Djinni()
        self.profile = Profile()
        try:
            from private.indeed import Indeed
            self.indeed = Indeed(profile=profile)
        except ImportError:
            pass
        except ModuleNotFoundError:
            pass

    def manual_authorization(self):
        self.djinni.manual_authorization()

def main():
    Fire(Octoffers)
