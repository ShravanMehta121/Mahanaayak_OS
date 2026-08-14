import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    if not os.path.exists("logs"):
        os.makedirs("logs", exist_ok=True)

    file_handler = RotatingFileHandler("logs/mahanaayak.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Mahanaayak OS startup")
