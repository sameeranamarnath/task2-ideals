import requests  
import os  
from dotenv import load_dotenv  
  
load_dotenv()  
  
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")  
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")  
FROM_EMAIL = os.getenv("FROM_EMAIL")  
  
def send_email(to_email, subject, text):  
    response = requests.post(  
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",  
        auth=("api", MAILGUN_API_KEY),  
        data={  
            "from": FROM_EMAIL,  
            "to": [to_email],  
            "subject": subject,  
            "text": text  
        }  
    )  
    response.raise_for_status()  
    return response.json()  