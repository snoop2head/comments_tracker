# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/youtube/v3/docs/commentThreads/list?apix_params=%7B%22part%22%3A%22snippet%2Creplies%22%2C%22videoId%22%3A%22_VB39Jo8mAQ%22%7D#usage
# totalResults are only for comments

import os
import googleapiclient.discovery
from urllib.parse import urlparse, parse_qs

def get_yt_video_id(url):
    if url.startswith(('youtu', 'www')):
        url = 'http://' + url

    query = urlparse(url)

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith(('/embed/', '/v/')):
            return query.path.split('/')[2]
    elif 'youtu.be' in query.hostname:
        return query.path[1:]
    else:
        raise ValueError


def ytbe_cmt_rply(video_url):
    # parsing user input domain

    video_query = get_yt_video_id(video_url)
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "your_youtube_API_developer_key"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        #snippet is regular comments
        #replies are replies to the comments
        part="snippet,replies",
        #maximum results according to newest first
        #maximum results can show up to 100 newest comments
        maxResults=100,
        videoId=video_query
    )
    response = request.execute()
    #items are arrayed in dictionary according to newest comments
    specific_response = response['items']
    no_of_response = str(len(specific_response))
    print('ytb.py - ' + no_of_response)
    return no_of_response
