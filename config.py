import os
import logging

# Azure DevOps Configuration
ORGANIZATION = "dorset-ics"
PROJECT = "DiiS%20Development%20Team"
BASE_URL = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}"

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('azure_devops_report.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def get_pat_from_file():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "pat.txt")
    try:
        with open(desktop_path, "r") as file:
            pat = file.read().strip()
            logging.info("PAT successfully retrieved")
            return pat
    except FileNotFoundError:
        logging.error("PAT file not found on desktop")
        raise
    except Exception as e:
        logging.error(f"Error reading PAT: {e}")
        raise