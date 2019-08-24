import os
from slack import RTMClient
import re
from slack_input_url_crawl_classify import check_overlap_data_and_classify
from pymongo import MongoClient
from db_check import give_data_with_comments

# mongodb setup
client = MongoClient('your_server_ip', 27017)
db = client.gaudio

# RTMClient serves the role as server
# RTMClient receive message only for channels

@RTMClient.run_on(event="message")
def say_hello(**payload):
  print("this is input - " + str(payload))
  data = payload['data']
  # print(data)
  web_client = payload['web_client']
  url_list = []

  # ignore inputted bot message: bot message also is recognized as a message in slack
  try:
    if data['subtype'] == 'bot_message':
      pass
  except:
    if data['text']:
      print('yes - ' + data['text'])
      channel_id = data['channel']
      thread_ts = data['ts']
      user = data['user']
      text = data['text']
      raw_urls = re.findall(r'(https?://[^\s]+)', text)
      print(raw_urls)
      # if there are no url types on the inputted chat, pass
      if not raw_urls:
          pass
      if "!check" in data['text']:
        string_to_return = ""
        for string in give_data_with_comments():
          string_with_line_break = string + "\n"
          string_to_return += string_with_line_break
        web_client.chat_postMessage(
              # specify channel
              channel=channel_id,
              # reply text
              text=f"<@{user}>," + string_to_return,
              # reply as a thread
              thread_ts=thread_ts
            )

      else:
          for url in raw_urls:
            clean_url = url[:-1]
            # insert on mongodb
            type_data = check_overlap_data_and_classify(clean_url)
            if not type_data:
              web_client.chat_postMessage(
                # specify channel
                channel=channel_id,
                # reply text
                text=f"<@{user}>, this website is already being monitored. Don't worry! I got this.",
                # reply as a thread
                thread_ts=thread_ts
              )
            if type_data:
              db.type.insert_one(type_data)

              web_client.chat_postMessage(
                # specify channel
                channel=channel_id,
                # reply text
                text=f"<@{user}>, website "+ clean_url +" that you sent will be monitored",
                # reply as a thread
                thread_ts=thread_ts
              )
    else:
      pass

# gaudio slack token
slack_token = "your_slack_token"
rtm_client = RTMClient(
  token=slack_token,
  connect_method='rtm.start'
)
rtm_client.start()
