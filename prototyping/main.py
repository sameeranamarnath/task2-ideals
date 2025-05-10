import lever_client, ai_matching, mailgun_client  
import os, logging  
from dotenv import load_dotenv  
  
load_dotenv()  
CALENDLY_LINK = os.getenv("CALENDLY_LINK")  
  
logging.basicConfig(level=logging.INFO)  
  
def main():  
    try:  
        candidates = lever_client.get_candidates()["data"]  
        postings = lever_client.get_postings()["data"]  
  
        candidate = candidates[0]  # For demo purposes  
        posting = postings[0]  
  
        candidate_profile = {  
            "name": candidate["name"],  
            "email": candidate["emails"][0],  
            "resume": f"{candidate.get('headline', '')}\n{candidate.get('summary', '')}"  
        }  
  
        posting_details = {  
            "title": posting["text"],  
            "description": posting.get("descriptionPlain", "")  
        }  
  
        logging.info(f"Evaluating '{candidate_profile['name']}' for role '{posting_details['title']}'.")  
  
        analysis_result = ai_matching.candidate_match_analysis(candidate_profile, posting_details)  
        print("\nAI Talent Specialist Evaluation:\n", analysis_result)  
  
        approval = input("\nMove candidate forward to next stage? (y/n): ").strip().lower()  
  
        if approval == 'y':  
            lever_client.update_candidate_status(candidate["id"], "phone-screen")  
            email_body = f"""Hello {candidate_profile['name']},  
  
Great news! We'd like to move forward with your application for '{posting_details['title']}'.  
  
Please schedule your next interview at your convenience via this link:  
{CALENDLY_LINK}  
  
Looking forward to speaking with you soon!  
  
Best regards,  
Talent Acquisition Team"""  
  
            mailgun_client.send_email(candidate_profile["email"], "Next Steps in Your Application", email_body)  
            logging.info("Candidate status updated and email sent.")  
        else:  
            lever_client.update_candidate_status(candidate["id"], "rejected")  
            logging.info("Candidate marked as rejected.")  
  
    except Exception as e:  
        logging.error(f"An error occurred: {e}")  
  
if __name__ == "__main__":  
    main()  