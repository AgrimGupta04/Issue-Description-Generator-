import requests
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

# GitHub Repository Details
GITHUB_OWNER = "langchain-ai"
GITHUB_REPO = "langchain"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM using OpenAI-compatible API
llm = ChatOpenAI(
    model="mixtral-8x7b-32768",  # Example Groq model
    openai_api_key=GROQ_API_KEY,  # Replace with your Groq API key
    base_url="https://api.groq.com/openai/v1"
)

def fetch_github_issues():
    """Fetches the first 5 open issues from the GitHub repository."""
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/issues?state=open&per_page=5"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()[:5]  # Get first 5 issues
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def generate_issue_description(title, body):
    """Generates an improved description for a GitHub issue using Groq LLM."""
    prompt = f"Enhance and summarize the following GitHub issue:\n\nTitle: {title}\nDescription: {body}"
    response = llm.invoke(prompt)  # Get the response object
    return response.content if hasattr(response, "content") else str(response)

def main():
    issues = fetch_github_issues()
    
    if not issues:
        print("No issues found or API error.")
        return
    
    print("\n### First 5 GitHub Issues with Enhanced Descriptions ###\n")
    
    for issue in issues:
        issue_number = issue.get("number")
        title = issue.get("title", "No Title")
        body = issue.get("body", "No Description Available")
        
        improved_description = generate_issue_description(title, body)
        
        print(f"Issue #{issue_number}: {title}")
        print(f"Enhanced Description:\n{improved_description}")
        print("-" * 80)

if __name__ == "__main__":
    main()
