import os
import pathlib

from .scraper import Scraper
from .tweezer import Tweezer

class Bot:

    def __init__(self):
        self.scraper = Scraper()
        self.tweezer = Tweezer()

    def scrape_jobs(self, old_jobs):
        # Get the job posts as set that consists of tuples of job key and link
        try:
            jobs = self.scraper.get_jobs()
        except:
            print('TU job server down. Could not get the jobs')
            jobs = set()

        # old_jobs = self.scraper.readFile(os.path.join(pathlib.Path(os.path.abspath(__file__)).parent, 'jobs.txt'))
        try:
            old_jobs = self.scraper.readBlob(old_jobs)
        except:
            print('Could not read the blob')
            # If reading the old jobs fails, the program will tweet shit load of jobs, this stops that
            old_jobs = jobs

        return jobs, old_jobs

    def prepare_jobs(self, jobs, old_jobs, job_type):
        
        if job_type == 'new':
            p_jobs = self.scraper.extract_new_jobs(jobs, old_jobs)
        elif job_type == 'ending':
            p_jobs = self.scraper.extract_ending_jobs(jobs)
        
        # Get the newly posted job descriptions
        info_p_jobs = []
        for job in p_jobs:
            fields, description, desires = self.scraper.get_the_job(job[1])
            info_p_jobs.append([fields, description, desires, job[1]])       
        
        return info_p_jobs

    def tweet_tweet(self, info_jobs, job_type):
        # Tweet the new jobs
        for job in info_jobs:
            content = self.tweezer.prepare_job_content(job, job_type)
            try:
                status = self.tweezer.tweet(content)
            except Exception as e:
                print(e)
        
    def write_jobs(self, jobs, file_name):
        # Write the newly fetched jobs to file
        self.scraper.writeToBlob(jobs, file_name)
        # self.scraper.writeFile(jobs, os.path.join(pathlib.Path(os.path.abspath(__file__)).parent, file_name))

