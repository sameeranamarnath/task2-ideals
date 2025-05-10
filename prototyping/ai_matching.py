import os  
from langchain.chat_models import AzureChatOpenAI  
from langchain.prompts import ChatPromptTemplate  
from dotenv import load_dotenv  
  
load_dotenv()  
  
llm = AzureChatOpenAI(  
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),  
    temperature=0.2  
)  
  
def candidate_match_analysis(candidate, posting):  
    prompt_template = ChatPromptTemplate.from_template(  
        """You are a senior Talent Specialist evaluating candidates for the role '{role_title}'.  
  
        Candidate Profile:  
        Name: {candidate_name}  
        Email: {candidate_email}  
        Resume/Details: {candidate_resume}  
  
        Job Posting Description:  
        {job_description}  
  
        Carefully assess the candidate's suitability for this role. Provide your evaluation clearly structured as follows:  
  
        Recommendation: [Suitable / Not Suitable]  
        Reasoning: [Brief explanation of your recommendation]"""  
    )  
  
    prompt = prompt_template.format_messages(  
        role_title=posting["title"],  
        candidate_name=candidate["name"],  
        candidate_email=candidate["email"],  
        candidate_resume=candidate["resume"],  
        job_description=posting["description"]  
    )  
  
    response = llm.invoke(prompt)  
    return response.content  