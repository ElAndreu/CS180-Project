# CS180-Project-Job-Matcher-AI-Agent
This Repository is for the cs180 final project and overall learning about how to incorportate A.I.

# Job Matcher AI Agent

An AI‑driven resume parser and job matcher built with CrewAI and Adzuna.  
Given a candidate’s resume (PDF), it:

1. **Parses** out skills, experience, and education.  
2. **Fetches** relevant job postings from Adzuna.  
3. **Ranks** them locally by keyword overlap.  
4. Returns the single best match as JSON.

---



## Installation

NOT PROVIDED

## Enpoints

1. Resume Parsing
2. Fetching jobs
3. Ranking Jobs

These are done by the run_agent which is what allows it to be done sequentially. 

## Authentication Requirements 
1. OpenAI key is a must and required in order to use the LLM, this is used by being assiend the OPEN_API_KEY attribute. This is also given to CrewAI.
   In this case, what we use is GPT-3.5-turbo.
2. We utulize he Adzuna API Credentials here as well.
     These are used in order for us to reach to Adzuna and seek that open sourced job board.
When one of these are missing, this program should not be functional and will throw out a runtime error. 
