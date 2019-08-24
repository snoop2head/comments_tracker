from pymongo import MongoClient
from datetime import date, datetime, timedelta
from crawler_Youtube import ytbe_cmt_rply
from crawler_facebook_iframe import facebook_slow_scroll_and_crawl_multiple_iframes
from crawler_disqus_updated import disqus_slow_scroll_and_crawl_multiple_iframes
from crawler_livere import platum, livere_slow_scroll_and_crawl_multiple_iframes

#today's date
today_int = date.today()
print("test_app - Today's date:", today_int)
today_str = str(today_int)

#mongodb setup
client = MongoClient('your_server_ip', 27017)
db = client.gaudio

# all data in archive collection
archive_col = db.archive.find()

# all data in concert collection
comment_col = db.comment.find()

# establishing url_type collection
type_col = db.type.find()

#how do i get all the urls from url type collection and make it into list?
url_list = []

# crawling comment section data from websites function
# data format is following:
# url_type_data is {url, domain, url_type}
# comment_section_data is {url, no_of_comment, input_date}
def crawl_now_comment_sections(url):
    data_from_type = db.type.find_one({'url':url})
    print('daily_crawl.py - ' + str(data_from_type))
    item_url_type = data_from_type['type']
    if item_url_type == 'youtube':
        no_of_comments = ytbe_cmt_rply(url)
    elif item_url_type == 'fbplugin':
        no_of_comments = facebook_slow_scroll_and_crawl_multiple_iframes(url)
    elif item_url_type == 'disqus':
        no_of_comments = disqus_slow_scroll_and_crawl_multiple_iframes(url)
    elif item_url_type == 'platum':
        no_of_comments = platum(url)
    elif item_url_type == 'livere':
        no_of_comments = livere_slow_scroll_and_crawl_multiple_iframes(url)
    print('daily_crawl.py - ' + str(no_of_comments))
    return no_of_comments

# storing crawled data on server temporalily
def update_comment_collection():
    # drop the comment col
    db.comment.drop()

    # update the comment col
    for data in type_col:
        url = data['url']
        now_comment_no = crawl_now_comment_sections(url)
        db.comment.insert_one({'url':url, 'no_of_comment':now_comment_no, 'input_date':today_str})

# update_comment_collection()

def update_youtube_only():
    youtube_col = db.type.find({'type':'youtube'})
    for data in youtube_col:
        url = data['url']
        now_comment_no = crawl_now_comment_sections(url)
        db.comment.insert_one({'url':url, 'no_of_comment':now_comment_no, 'input_date':today_str})

# update_youtube_only()


