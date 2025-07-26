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

## What is needed
Well, first you are definitely going to need your resume. 
--One of the main things that it will ask you for is the file path for that resume PDF.
-From here it gathers: 
1. Your Skills
2. Your Experience
3. Your Education

a small example of what the path can look like: "/home/user/resume.pdf"

-Another thing we use is the keywords gathered from the resume. These will be able to gather inforation to try and find the best compatible job that our AI agent can find in Adzuna. 

E.G. If you have python, it will look for positions that have python as a requirement. 

## DISCLAIMAER. I was not able to fully finish the project because I was using too much LLM and it requested me to change my plan. It did the same thing for gemini :( 
