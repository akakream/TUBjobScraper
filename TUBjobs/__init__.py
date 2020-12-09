import datetime
import logging

import azure.functions as func

from .bot import Bot

def main(mytimer: func.TimerRequest, inputblob: str,
         outputblob: func.Out[str]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    bot = Bot()
    
    jobs, old_jobs = bot.scrape_jobs(inputblob)
    
    info_new_jobs = bot.prepare_jobs(jobs, old_jobs, 'new')
    
    info_ending_jobs = bot.prepare_jobs(jobs, old_jobs, 'ending')
    
    bot.tweet_tweet(info_new_jobs, 'new')
    
    bot.tweet_tweet(info_ending_jobs, 'ending')
    
    bot.write_jobs(jobs, outputblob)
    