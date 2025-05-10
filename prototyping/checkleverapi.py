import requests
import os
from requests.auth import HTTPBasicAuth

import lever_client

# Manually parsed the .env file and populate os.environ to get the Lever API key
with open(".env", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            key, value = line.split("=", maxsplit=1)
            os.environ[key] = value.strip('"')

LEVER_API_KEY = os.getenv("LEVER_API_KEY")

candidates = lever_client.get_candidates()["data"]
print(candidates)

postings = lever_client.get_postings()["data"]
print(postings)

# for candidate in candidates:
#     application_id = candidate["applications"][0]
#     if application_id:
#         print(application_id)
#         data= lever_client.get_application_for_candidate(candidate["id"],application_id)
#         print(data)