from pymongo import MongoClient
from datetime import date, datetime, timedelta
import slack

# time right now
now_int = datetime.now()
now_str = str(now_int)
print('daily crawler - Right now it is ' + now_str)

#today's date
date_today = date.today()
print("test_app - Today's date:", date_today)
today_str = str(date_today)

# mongodb setup
client = MongoClient('your_server_ip', 27017)
db = client.gaudio

# all data in archive collection
archive_col = db.archive.find()

# all data in concert collection
comment_col = db.comment.find()

'''
# initial registration
db.archive.drop()
for data in comment_col:
    db.archive.insert_one(data)
'''



#slack token
slack_token = "slack_token"


def send_slack(url):
    if url:
        client = slack.WebClient(token=slack_token)
        client.chat_postMessage(
        channel="channel_name",
        text= "There is a new comment at: " + url
        )
    else:
        pass


def send_new_info(new_info_list):
    if not new_info_list:
        pass
    else:
        print('there is new information available')
        for data in new_info_list:
            send_slack(data['url'])


# data format is {url, no_of_comment, input_date}
def new_comment_info_list():
    new_info_list = []
    # finding difference based on comment col data
    for data in comment_col:
        index_url = data['url']

        # now data from comment col
        no_of_now_comments = data['no_of_comment']

        # previous data from archive col
        existed_archive_data = db.archive.find_one({'url':index_url})


        # when user updated a new url
        if not existed_archive_data:
            db.archive.insert_one(data)

        if existed_archive_data:
            no_of_previous_comments = existed_archive_data['no_of_comment']
            # when previous comments are same as comments of now
            if no_of_now_comments == no_of_previous_comments:
                pass

            # when previous comment numbers are different from comments of now
            else:
                print("db_daily_sorter - this is changed comment data: " + str(data))
                db.archive.update_one({'url':index_url},{'$set': {'no_of_comment':no_of_now_comments}})
                new_info_list.append(data)
        print(new_info_list)
    print(len(new_info_list))
    return new_info_list

# send_new_info(new_comment_info_list())
