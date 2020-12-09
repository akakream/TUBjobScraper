import tweepy
from .secrets import C_KEY, C_SECRET, A_TOKEN, A_TOKEN_SECRET

class Tweezer():
    
    def __init__(self):
        self.auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
        self.auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
        # Create API object
        self.api = tweepy.API(self.auth)
    
    def prepare_job_content(self, job, job_type):
        content = ''
        if job_type == 'new':
            content += '📜 ' + '𝗡𝗘𝗪 𝗝𝗢𝗕!' + ' 📜'  + '\n'
        elif job_type == 'ending':
            content += '😱 ' + '𝗟𝗔𝗦𝗧 𝗖𝗛𝗔𝗡𝗖𝗘 𝗧𝗢 𝗔𝗣𝗣𝗟𝗬!' + ' 😱' + '\n'
        content += f'𝗙𝗮𝗰𝘂𝗹𝘁𝘆: {job[0][0][1]}\n' 
        content += f'𝗠𝗼𝗻𝘁𝗵𝗹𝘆 𝗪𝗼𝗿𝗸 𝗛𝗼𝘂𝗿𝘀: {job[0][5][1].split(" ")[0]}\n' 
        content += f'𝗔𝗽𝗽𝗹𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗗𝗲𝗮𝗱𝗹𝗶𝗻𝗲: {job[0][9][1]}\n'
        content += f'𝗡𝘂𝗺𝗯𝗲𝗿 𝗼𝗳 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻𝘀: {job[0][4][1]}\n'
        content += f'𝗟𝗶𝗻𝗸: {job[3]}' # link to the job
        
        # Just in case that the tweet is more than 280 characters
        if len(content) > 280:
            content = ''
            if job_type == 'new':
                content += '📜 ' + '𝗡𝗘𝗪 𝗝𝗢𝗕!' + ' 📜'  + '\n'
            elif job_type == 'ending':
                content += '😱 ' + '𝗟𝗔𝗦𝗧 𝗖𝗛𝗔𝗡𝗖𝗘 𝗧𝗢 𝗔𝗣𝗣𝗟𝗬!' + ' 😱' + '\n'
            content += f'𝗙𝗮𝗰𝘂𝗹𝘁𝘆: {job[0][0][1]}\n' 
            content += f'𝗠𝗼𝗻𝘁𝗵𝗹𝘆 𝗪𝗼𝗿𝗸 𝗛𝗼𝘂𝗿𝘀: {job[0][5][1].split(" ")[0]}\n' 
            content += f'𝗔𝗽𝗽𝗹𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗗𝗲𝗮𝗱𝗹𝗶𝗻𝗲: {job[0][9][1]}\n'
            content += f'𝗟𝗶𝗻𝗸: {job[3]}' # link to the job
            
        return content

    def tweet(self, content):
        status = self.api.update_status(content)