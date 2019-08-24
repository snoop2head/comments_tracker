from daily_crawl import update_comment_collection
from daily_db_compare import send_new_info, new_comment_info_list

# first, update comment collection
update_comment_collection()

# second, update archive collection
# third, send the new comment information to slack chatbot
send_new_info(new_comment_info_list())
