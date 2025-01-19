import logging

log = logging.getLogger()

logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
    datefmt="%h %d %H-%m-%S",
)
