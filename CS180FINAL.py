import os
import sys
from dotenv import load_dotenv
import pdfplumber
from typing import List
from crewai import Agent, Crew, Task, Process
from crewai.tools import tool
import requests
#load up and import everything we need


load_dotenv() #load environment and grab all necessary api keys.
CREWAI_API_KEY = os.getenv("CREWAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

if not CREWAI_API_KEY:#make sure that we have all the keys,
    raise RuntimeError("…")
if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment or .env file")


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY #we use openai 

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

@tool("parse_resume")#using the tool, it should get info from pdf. 
def parse_resume(pdf_path: str) -> dict:
    """
    Extract skills, experience, and education sections from a resume PDF.
    """
    info = {"skills": [], "experience": [], "education": []}
    with pdfplumber.open(pdf_path) as pdf: #opens the pdf that is uploaded
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return info


@tool("fetch_jobs") #we get the jobs from adzuna using this tool and the API 
def fetch_jobs(keywords: List[str]) -> List[dict]:
    """
    Fetch job postings that match a list of keywords.
    """
    # TODO: IMPLEMENT HOW TO GET THE DATABASE
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY: #ensures Adzuna api key is used.
      raise RuntimeError("Please set ADZUNA_APP_ID and ADZUNA_APP_KEY in your environment or .env file")

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params={
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": " ".join(keywords),
        "results_per_page": 1,
    }#my api stuff 

    resp = requests.get(url, params=params) #get it one more time
    resp.raise_for_status()
    results = resp.json().get("results", [])
    jobs = []
    for job in results:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "url": job.get("redirect_url"),
        })
    return jobs


@tool("rank_jobs") #since there was problems with 5... 3.... 2... reach only 1 job now
def rank_jobs(parsed: dict, jobs: List[dict]) -> List[dict]:
    """
    Rank job postings by keyword overlap using local ranking logic.
    """
    return rank_jobs_local(parsed, jobs)

#------------------------------------------------------------------------------
#LOCAL NOT AI TESTING
#------------------------------------------------------------------------------

def rank_jobs_local(parsed: dict, jobs: List[dict]) -> List[dict]:
    """
    Simple keyword-overlap ranking: count how many resume keywords appear in the job title.
    """
    keywords = set(kw.lower() for kw in parsed.get("skills", []) + parsed.get("experience", []))
    scored = []
    for job in jobs:
        title_text = job.get("title", "").lower()
        score = sum(1 for kw in keywords if kw in title_text)
        scored.append((score, job))
    # sort descending by score and take top 5
    return [job for _, job in sorted(scored, key=lambda x: x[0], reverse=True)][:5]



# def run_local(pdf_path: str):
#     """Run parsing, fetching, and local ranking without calling the LLM."""
#     # Directly call the plain functions, not tool primitives
#     parsed = parse_resume(pdf_path)
#     print("Parsed resume sections:", parsed)

#     jobs = fetch_jobs(parsed.get("skills", []) + parsed.get("experience", []))
#     print("Fetched jobs:", jobs)

#     top5 = rank_jobs_local(parsed, jobs)
#     print("Top 5 ranked jobs (local):")
#     for job in top5:
#         print(f"- {job['title']} at {job['company']} ({job['url']})")

# -----------------------------------------------------------------------------
# crew and agent
# -----------------------------------------------------------------------------

matcher = Agent( #AI agent is set up here, now specify it muchacho. 
    backstory="You are an AI assistant specialized in matching candidate resumes to relevant job openings.",
    role="Job Matcher",
    goal="Extract, fetch, and rank jobs",
    tools=[parse_resume, fetch_jobs, rank_jobs],
    llm="gpt-3.5-turbo",
    memory=True,       
    verbose=True       
)

task = Task(
    description=(
        "Parse the resume PDF, fetch matching job postings, and rank them locally using the rank_jobs tool; "
        "return exactly the list of ranked job dicts (title, company, location, url) with no explanations or extra text."
    ),
    agent=matcher,
    expected_output="A list of job dicts in ranked order, with no explanations."

)

crew = Crew(
    agents=[matcher],
    tasks=[task],
    process=Process.sequential,
    verbose=True
)


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

def run_agent(pdf_path: str):
    result = crew.kickoff(inputs={"pdf_path": pdf_path})
    print("\n=== Recommended Jobs ===")
    print(result)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) == 2 else input("Path to resume PDF: ")
    run_agent(path)
    # run_local(path)

# parsed = parse_resume._run("/content/AndreyResume2026.pdf") these were tests to make sure that the code was working.
# print("Parsed resume sections:", parsed)

# # 2) Fetch jobs (stub)
# jobs = fetch_jobs._run(parsed["skills"] + parsed["experience"])
# print("Stubbed job list:", jobs)