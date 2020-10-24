#!/usr/bin/env python
# coding: utf-8

# #  Job Hunt Skills
# ## Using Python, Pandas, Plotly, Requests, and Beautiful Soup
# ### branched from Jeff Hale's Data Science Skills Code
# ### 2020 October 20

# Import necessary libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import matplotlib.pyplot as plt
import datetime

# # Objective
# Show prioritization of skills for certain jobs
# This will be based on regularly scraped data from online job listings.
# Initially start with Indeed, Dice, Monster, SimplyHired.
# Glassdoor and # AngelCo , LinkedIn with dynamic content will be a later iteration 
# 
# A legal footnote about scraping:
# Basically, LinkedIn's claim that HiQ Labs scraping action constituted hacking was ruled incorrect based on the CFAA (Computer Fraud and Abuse Act) given the information scraped is basically public and HiQ (or any scraper) did not create any substantial circumvention of any authorized access (the job listing is not even protected by username/password).
# https://cdn.ca9.uscourts.gov/datastore/opinions/2019/09/09/17-16783.pdf
# 

# ## Scrape the data from Online Job Sites
# The header to pass and the search terms to iterate through with "<job title>" are below.
# Add other search terms if you like.

ERR_VALUE = 0
WEB_TIMEOUT = 10

DEBUG = 16
ERROR = 8
WARN  = 4
INFO  = 2
QUIET = 0

verbose = DEBUG

def verbose(level, msg):
    """
        control how much console information is shown
        improve sophistication later
    """ 
    if (level & DEBUG):
        print(msg)
    elif (level & INFO):
        print(msg)
    return

def SaveData(filename, save_list, file_header="LIST"):
    """
     IMPORTANT: for convenience the first skill entry is NULL STRING by design for generic skill query 
    """
    tdf = pd.DataFrame({file_header:save_list})
    tdf = tdf.fillna('deliberately_null')
    verbose(INFO, "\nSaving ... " + filename)
    tdf.to_csv(filename, index=False, header=True)
    return

def LoadData(filename):
    """
    Load CSV and return a list e.g. of skills or jobs
    >>> listOfSkills = LoadData("Skill_2020-10-20")
    """
    tdf = pd.read_csv(filename)
    verbose(INFO, "\nLoading ... "+filename)
    tdf = tdf.apply(lambda x:x.str.replace('deliberately_null', '').astype(object), axis=1)
    tdf = tdf.fillna('')
    # assume significant list is always first column
    return list(tdf[tdf.columns[0]])

# -----------------------------------------------------------------------------------------

# do extra study on User-Agent and other header information relevant to web requests
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

# # Indeed
def ScrapeIndeed(job_titles, search_terms, location):
    """
        Specialized Scrape Logic specific to Indeed.com job listing site format
        returns count per skills/search_terms psoted for job_titles in location
        
        for Exception cases e.g. text not found if timedout connection or search failed
        we append ERR_VALUE to list, to make sure the list from search terms are of equal length
        and we can even manually back fetch data later
    """
    verbose(INFO,"\n### Analyzing Indeed.com ###")
    for job in job_titles:
        indeed_list=[]
        for term in search_terms:
            url = f'https://www.indeed.com/jobs?q=%22{job}%22+%22{term}%22&l={location}'
            verbose(DEBUG, "\tSearching skill [{t}] for Job=[{j}]...".format(t=term,j=job))
            try:
                r = requests.get(url, headers=header, timeout=WEB_TIMEOUT)
                soup = bs(r.text, 'html.parser')
                count_str = soup.find('div', id="searchCountPages").get_text()
                numb = count_str.split()
                # replace all commas in the number string to make it ok to convert to integer
                nresults = numb[-2].replace(",","")
                indeed_list.append(int(nresults))
            except Exception as e:
                indeed_list.append(ERR_VALUE)  # always add to list so each search term has an entry even when not found 
                verbose(INFO, f'error: {e}')
    return indeed_list

# # Monster
def ScrapeMonster(job_titles, search_terms, location):
    verbose(INFO, "\n### Anayzing Monster.com ###")
    for job in job_titles:
        monster_list = []
        for term in search_terms:
            # Monster.com assumes USA location - let us do location here some other time
            url = f'https://www.monster.com/jobs/search/?q=__22{job}__22-__22{term}__22'
            verbose(INFO, "\tSearching skill [{}] for Job=[{}]...".format(term, job))
            try:
                r = requests.get(url, headers=header, timeout=WEB_TIMEOUT)
                soup = bs(r.text, 'html.parser')
                count_str = soup.find('h2', class_="figure").get_text()
                numb = count_str.split()
                # cannot just convert to int count_str due to fancy formats e.g. with comma etc.
                monster_count = numb[0].replace("(", "")
                monster_list.append(int(monster_count))
            except Exception as e:
                monster_list.append(ERR_VALUE) # always add to list so each search term has an entry even when not found 
                verbose(INFO, f'error: {e}')
    return monster_list

# # SimplyHired

def ScrapeSimplyHired(job_titles, search_terms, location):
    verbose(INFO, "\n### Analyzing SimplyHired.com ###")
    for job in job_titles:
        simply_list = []
        for term in search_terms:
            url = f'https://www.simplyhired.com/search?q=%22{job}%22+%22{term}%22&l={location}'
            verbose(DEBUG, "\tSearching skill=[{}] for Job=[{}]...".format(term, job))
            try:
                r = requests.get(url, headers=header, timeout=WEB_TIMEOUT)
                soup = bs(r.text, 'html.parser')
                count_str = soup.find('span', class_="CategoryPath-total").get_text()
                # each job site has its own fancy formats for job count e.g. with comma etc.
                count_str = count_str.replace(",","")
                simply_list.append(int(count_str))
            except Exception as e:
                simply_list.append(ERR_VALUE) # always add to list so each search term has an entry even when not found
                verbose(INFO, f'error: {e}')
    return simply_list

def ScrapeSites(job_titles, search_terms, location, output_file="data.csv"):
    """
        Assemble the dataframe tabulation of jobs skills and sites and write out to file
    """
    df = pd.DataFrame(index=search_terms)
    # Changes to special characters, e.g. C# and C++ as these get escaped in query strings**
    # ** change C# as ASCII C%23 and C++  as ASCII C%2B%2B will be universally ok*
    # two styles of replacing special characters for C# and C++
    search_terms= [term.replace("+","%2B") for term in search_terms]
    search_terms = list(map(lambda st : str.replace(st, "#","%23"),search_terms))

    df['Indeed'] =  ScrapeIndeed(job_titles, search_terms, location)
    df['Monster'] = ScrapeMonster(job_titles, search_terms, location)
    df['SimplyHired'] = ScrapeSimplyHired(job_titles, search_terms, location)
    # temporarily assume one job_tile and use that as heading for skills index
    df.rename(index={'':job_titles[0]}, inplace=True)
    verbose(INFO, "Number of Skills:{} Catalogued :{} rows of {} entries".format(len(search_terms), len(df), df.size))
    # This process below is not necessary if integer conversion is done during each search
    #   The advantage below is it is a more efficient batch conversion assuming we only worry about comma
    #   df = df.apply(lambda x:x.str.replace(',', '').astype(int32), axis=1)
    df.head()
    df.to_csv(output_file)
    return df

def ScrapeJobs():
    # data.csv format: include in filename context of data
    today = datetime.date.today()
    # improve this later - temporarily look for Data Scientist job
    job_header = "Position"
    job_file = f'Jobs_{today}.csv'
    skill_header = "Skills"
    skill_file = f'{skill_header}_{today}.csv'
    search_terms = LoadData(skill_file)

    # job_titles = LoadData(job_file)
    # use hard coded job and location first
    job_titles=["Data Scientist"]
    job = job_titles[0]
    location = "United States"
    data_file = f'{job}_{location}_{today}.csv'
    ScrapeSites(job_titles, search_terms, location, data_file)
    return

def main():
    # ----- Assume these files were saved originally   
    # SaveData(skill_file, search_terms, skill_header)
    # SaveData(job_file, job_titles, job_header)
    # --------------------------
    verbose( INFO, "\nLet us go job hunting...")
    ScrapeJobs()

if __name__ == "__main__" : main()