from bs4 import BeautifulSoup
import requests
from datetime import datetime

class Scraper:
    
    def __init__(self):
        self.url = 'http://virtual-prsb.service.tu-berlin.de/AD/list.php'
        self.HOST = 'http://virtual-prsb.service.tu-berlin.de/AD/'
        self.source = requests.get(self.url)
        self.soup = BeautifulSoup(self.source.text, 'lxml')
    
    def get_jobs(self):

        jobs = set()

        table = self.soup.table
        table_rows = table.find_all('tr')

        for row in table_rows:
            
            # If the row is a Faculty header, skip it 
            if row.th:
                continue
            
            # Get the key and link of every job available in a tuple
            columns = row.find_all('td')
            job = (columns[0].text, self.HOST + columns[0].a['href'], columns[3].text)
            
            jobs.add(job)

        return jobs
        

    def get_the_job(self, jobURL):
        source = requests.get(jobURL)    
        soup = BeautifulSoup(source.text, 'lxml')
        
        # Get the texts about the job
        match = soup.find('div', class_='col-xs-12 col-sm-8 col-md-8 col-lg-9')
        ps = match.find_all('p')
        description = ps[1].text 
        desires = ps[2].text
        
        # Get facts about the job
        match = soup.find('div', class_='col-xs-12 col-sm-4 col-md-4 col-lg-3')
        ps = match.find_all('p')
        job_fields = []
        for el in ps:
            value = el.text.replace('\t', '')
            value = value.strip('\n')
            value = value.split('\n')
            job_fields.append(value)
        
        return job_fields, description, desires

        
    def readFile(self, filename):
        '''
        Reads jobs line by line from file and puts them into tuples.
        Then into a set.
        '''
        
        jobs = set()
        
        with open(filename, 'r') as f:
            for line in f:
                # The key and link is splitted with :::
                pair = line.split(':::')
                # Do not read the \n at the end of the line
                tup = (pair[0], pair[1], pair[2][:-1])
                jobs.add(tup)
        
        return jobs
    
    def readBlob(self, blob):
        '''
        Reads jobs line by line from file and puts them into tuples.
        Then into a set.
        '''
        
        jobs = set()
        
        for line in blob.split('\n')[:-1]:
            # The key and link is splitted with :::
            pair = line.split(':::')
            # Do not read the \n at the end of the line
            tup = (pair[0], pair[1], pair[2])
            jobs.add(tup)
        
        return jobs
    
    def writeFile(self, data, filename):
        '''
        Write the fetched jobs into file.
        '''
        
        # Clean the content before writing into
        self.deleteContent(filename)
        with open(filename, 'a') as f:
            for d in data:
                key = d[0]
                link = d[1]
                date = d[2]
                # Split key and link with ::: for convenience when reading
                f.write(f'{key}:::{link}:::{date}\n')

    def writeToBlob(self, data, blob):
        
        jobdata = ''
        for d in data:
            key = d[0]
            link = d[1]
            date = d[2]
            # Split key and link with ::: for convenience when reading
            job = f'{key}:::{link}:::{date}\n'
            jobdata += job
            
        blob.set(jobdata)

    def deleteContent(self, filename):
        with open(filename, 'w') as f:
            f.close()


    def extract_new_jobs(self, jobs, old_jobs):        
        # Compare the newly feyched jobs with the present jobs, get the difference
        jobs_no_date = {job[:2] for job in jobs}
        old_jobs_no_date = {job[:2] for job in old_jobs}
        new_jobs = jobs_no_date.difference(old_jobs_no_date)

        return new_jobs
    
    
    def extract_ending_jobs(self, jobs):
        # Get the jobs that are ending
        current_date = datetime.today().strftime('%d.%m.%Y')
        
        ending_jobs = set()
        
        for job in jobs:
            try:
                cur_date = datetime.strptime(current_date, '%d.%m.%Y')        
                job_date = datetime.strptime(job[2], '%d.%m.%Y')        
                rest = abs((job_date - cur_date).days)
                if rest == 1:
                    ending_jobs.add(job)
            except:
                # print('Dauerausschreibung')
                pass
        
        return ending_jobs
            
