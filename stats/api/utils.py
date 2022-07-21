import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

GITHUB_TOKEN = f"token {os.environ.get('GITHUB_TOKEN')}"
DAYS_IN_YEAR = 365
