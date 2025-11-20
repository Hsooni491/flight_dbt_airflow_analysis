import logging
import os

LOG_FILE_PATH = os.path.join(
    os.path.dirname(__file__),  
    "project_logs.log"    # The file where ALL logs will go
)

def setup_project_logger():
    logger = logging.getLogger("myproject")  # Custom logger ✔
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler("project.log")
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger