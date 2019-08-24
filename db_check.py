from pymongo import MongoClient

def give_data_with_comments():
    #mongodb setup
    client = MongoClient('your_server_ip', 27017)
    db = client.gaudio

    # all data in archive collection
    archive_col = db.archive.find()

    strings_with_comments_list = []

    for data in archive_col:
        url = data['url']
        no_of_comment = data['no_of_comment']
        if int(no_of_comment) > 0:
            print("db_check - " + str(data) + "has comments in it")
            useful_string = url + " - " + no_of_comment + " comments"
            strings_with_comments_list.append(useful_string)
    return strings_with_comments_list



