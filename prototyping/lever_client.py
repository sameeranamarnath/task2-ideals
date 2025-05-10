# lever_client.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "https://api.sandbox.lever.co/v1"
# Manually parsed the .env file and populate os.environ to get the lever api key
with open(".env", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", maxsplit=1)
            os.environ[key] = value.strip('"')

API_KEY = os.getenv("LEVER_API_KEY") #works

auth = (API_KEY, '')

def get_candidates():
    response = requests.get(f"{API_BASE_URL}/candidates", auth=auth)
    response.raise_for_status()
    return response.json()

def get_postings():
    response = requests.get(f"{API_BASE_URL}/postings", auth=auth)
    response.raise_for_status()
    return response.json()


def get_application_for_candidate(candidate_id,application_id):
    response = requests.get(f"{API_BASE_URL}/candidates/{candidate_id}/applications/{application_id}", auth=auth)
    response.raise_for_status()
    return response.json()
