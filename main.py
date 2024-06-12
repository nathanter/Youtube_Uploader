import time
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.errors
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os


folder = ""
folder = input("type folder name : ")
fnames = []
for x in os.listdir("./"+folder):
    fnames.append(x)


with open("./progressfile.txt") as f:
    
    index = int(f.read())




flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',
    scopes=[
        "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/youtube",
        "https://www.googleapis.com/auth/youtube.upload"
    ]
)
credentials = flow.run_local_server(host='localhost',
      port=8080, 
      authorization_prompt_message='Please visit this URL: {url}', 
      success_message='The auth flow is complete; you may close this window.',
      open_browser=True)

with build('youtube', 'v3', credentials=credentials) as youtube_service:

    while index<len(fnames):
        try:
            
            media = MediaFileUpload("./"+folder+"/"+fnames[index])
            
            
            print("executed")
            video_upload_sequence = youtube_service.videos().insert(
                part = "snippet",
                body = {"snippet":{"title":" " + fnames[index],
                                   "description":"published by Bulk Uploader on" + str(time.localtime().tm_year)+"/"+str(time.localtime().tm_mon)+"/"+str(time.localtime().tm_mday)
                                   ,"categoryId":1}},
                media_body = media

            )
            video_upload_sequence.execute()
            index += 1
            
            with open("./progressfile.txt",'w') as f:
                progress= str(index)
                f.write(progress)
            
        except googleapiclient.errors.Error:
            print("failure")
            cur = time.time()
            cur = time.localtime(cur)
            if cur.tm_min >= 30:
                cur = cur.tm_hour + 1

            else:
                cur = cur.tm_hour
            
            time_to_wait = 24 - cur

            time.sleep(time_to_wait*60*60)
    index = 0   
    with open("./progressfile.txt",'w') as f:
                progress= str(index)
                f.write(progress)
