from TUBjobs.tweezer import Tweezer

def test_thread():

    tweezer = Tweezer()
    
    info_jobs = ["test1", "test2", "test3"]    
    
    # Store the id of the previous tweet to tweet in a thread
    prev_id = None

    # Tweet the new jobs
    for job in info_jobs:
        content = job
        try:
            status = tweezer.tweet(content, prev_id)
            prev_id = status.id
        except Exception as e:
            print(e)