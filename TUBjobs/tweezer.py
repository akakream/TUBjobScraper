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
        
        if len(job[0][0][1]) < 100:
            content += f'Faculty: {job[0][0][1]}\n' 
        else:
            content += f'Faculty: {job[0][0][1][:100]}...\n' 
        
        if job[0][3][1] == 'Ja':
            content += f'Teaching: ✅\n'
        else:
            content += f'Teaching: ❌\n'
        
        content += f'# Hours/Month: {job[0][5][1].split(" ")[0]}\n' 
        content += f'# Positions: {job[0][4][1]}\n'
        content += f'Apply until: {job[0][9][1]}\n'

        # In the worst case the tweet will be 171 characters, excluding the faculty field value
        # Bold chars and emojis count 2
        # Link will be cropped only 48 chars are calculated
        content += f'Link: {job[3]}' # link to the job
        
        return content

    def tweet(self, content, prev_id):
        if prev_id is None:
            status = self.api.update_status(content)
        else:
            status = self.api.update_status(content, prev_id)

        return status