# Public Relations Article Tracker

- ### 시간과 돈을 들여서 홍보 자료들을 뿌렸으나, 홍보 자료들에 달리는 댓글들을 일일이 파악하기는 힘들다.

- ### 이제는 Slack Chatbot으로 홍보 게시물에 달리는 댓글들을 추적하고, 댓글 동향을 추적할 홍보글을 등록할 수 있다.

- ### 댓글 위젯으로 Disqus widget, livere widget, facebook widget을 장착한 모든 블로그 게시글들에 댓글들이 달릴 때마다 Slack으로 알림이 온다.

- ### Youtube 영상에 댓글이 올라오면 Slack으로 알림이 온다.

-------

## Slack Chatbot 파일, 함수 별 기능 설명

### app_slack.py

- [x] say_hello(**payload) 
  Slack에서 메시지 내용을 받는 역할을 수행한다. 
- 함수 자체 기능
  - URL이 담겨있는 Slack 메시지에다가 thread로 답변을 한다.
  - 만약 이전에 MongoDB에 등록된 URL이면 "this website is already being monitored"라는 메시지를  thread로 답변한다.
  - MongoDB에 등록되지 않은 URL이면 "this website will be monitored"라는 메시지를 thread로 답변한다. 메시지 중에서 URL 형식의 내용을 추출해내서 해당 URL을 MongoDB type 콜렉션에 저장한다.  
  - Slack 메시지 중에서 "!check"이 담겨있으면 이 메시지를 탐지한다. 답글이 달려있는 URL들이 포함된 리스트를 give_data_with_comments() 함수로 가져온 후, 이 리스트를 string으로 변환을 시킨 다음 해당 "!check"이 포함된 Slack 메시지에 thread로 답변을 단다. 
- Dependency
  - Slack 모듈의 RTMClient를 microframework로 쓰기 때문에 RTMClient로서 작동하는 동안에만 메시지를 받고, 답글을 다는 기능을 수행한다.
  - regex로 일반 텍스트와 URL을 분리한다. 

  - 메시지에서 받은 URL을 MongoDB에 입력할 수 있도록 pymongo 모듈의 MongoClient 함수를 이용한다. 
  - 같은 디렉토리의 slack_input_url_crawl_classify.py 파일에서 check_overlap_data_and_classify() 함수 
  - 같은 디렉토리의 db_check.py 파일에서 give_data_with_comments() 함수는 MongoDB에서 답글이 달린 URL들이 있는 list를 가져온다. 

### slack_input_url_crawl_classify.py

- [x] classifier(user_input_url): 해당 url에 달리는 덧글이 어떤 타입인지 분석한다.
- 함수 자체 기능
  - URL을 크롤링해서 youtube 타입인지 / platum 타입인지 / disqus 타입인지 / livere 타입인지 / facebook plugin을 이용하는 타입인지 분석한다. 
  - Type을 알아낸 이후 MongoDB에 추가할 수 있는 딕셔너리를 반환한다. 
    - 예시: {'url':user_input_url, 'domain':domain, 'type': 'disqus'} 
- Dependency
  - selenium 모듈과 selenium 웹드라이버로 크롤링을 한다. 
  - time 모듈로 크롤링을 할 때 웹페이지가 로딩되는 시간을 번다. 

- [x] check_overlap_data_and_classify(user_input_url): URL이 type 콜렉션에 새로 추가되야 할 URL인지, 아니면 이전에 존재하던 URL인지를 판단한다. 
- 함수 자체 기능
  - 먼저 MongoDB에서 type 콜렉션에 입력된 URL값인지 아닌지 파악한다. type 콜렉션에 존재하는 URL이면 아무 것도 반환하지 않는다. 
  - 만약 기존에 입력되지 않은 URL일 경우 type collection에 들어갈 딕셔너리를 classifier(user_input_url)을 이용해서 반환한다. 
- Dependency
  - MongoDB type 콜렉션에 존재하는 URL인지 파악하기 위해 pymongo 모듈의 MongoClient 함수를 이용한다. 
  - 같은 파일에서 classifier(user_input_url)을 이용해서 Type을 알아낸 이후 MongoDB에 추가할 수 있는 딕셔너리를 반환한다.
    - 예시: {'url':user_input_url, 'domain':domain, 'type': 'disqus'}

### db_check.py

- [x] give_data_with_comments() 
- 함수 자체 기능
  - MongoDB의 archive 콜렉션에 댓글 기록이 존재하는 딕셔너리들을 모두 가져오고, 댓글 기록이 존재하는 URL들을 모아서 하나의 리스트로 만든다. 
- Dependency
  - MongoDB의 archive 콜렉션의 데이터를 가져오기 위해 pymongo 모듈의 MongoClient 함수를 이용한다. 

________________________________________
## Public Relations Article Crawler 파일, 함수 별 기능 설명
### app.py

- [x] update_comment_collection(): 다섯 가지의 크롤러들을 동작시킴.
- 함수 자체 기능
  - Mongo DB의 Gaudio DB / type collection에 있는 URL들에 있는 댓글 정보들을 comment collection으로 긁어온다. 
- 의존하는 기능
  - (후에 서술하는) daily_crawl.py에서 import한 함수

- [x] send_new_info(new_comment_info_list()): 새로 달린 댓글 정보들을 슬랙 메시지로 보냄.
  - 함수 자체 기능
    - new_comment_info_list()는 새로운 댓글들이 달린 data 딕셔너리들의  리스트이다. 데이터의 형태는 {'url', 'no_of_comment', 'input_date'}이다. 
    - send_new_info(list_object)는 list_object의 모든 데이터들을 하나하나 슬랙으로 전송한다. 
  - Dependency 
    - daily_db_compare에서 import한 함수 두 개

### daily_crawl.py

- [x] crawl_now_comment_sections(url):크롤링 방식을 정하고 URL을 알맞은 크롤러에 배분한다. 

- 함수 자체 기능

  - 크롤링 방식은 Mongo DB의 Gaudio DB / type collection에 있는 데이터에 저장된 각 타입 정보에 따라서 정한다. 어떤 크롤러를 작동시키든 간에 결과값은 integer인 no_of_comments로 반환이 된다.

- 의존하는 기능

  - 함수 출처는 총 네 곳이며, import한 함수는 다섯 개이다. 타입은 다섯 가지 종류가 존재하는데, 이는 youtube, fbplugin, disqus, platum, livere이다. 이에 따라서 크롤러도 다섯 종류가 존재한다. 

    1. ytbe_cmt_rply(url)은 crawler_Youtube.py에서 import한 함수이다.

    2. facebook_slow_scroll_and_crawl_multiple_iframes(url)은 crawler_facebook_iframe.py에서 import한 함수이다.

    3. disqus_slow_scroll_and_crawl_multiple_iframes(url)은 crawler_disqus_updated.py에서 import한 함수이다.

    4. platum(url)은 crawler_livere.py에서 import한 함수이다.
    5. livere_slow_scroll_and_crawl_multiple_iframes(url)은 crawler_livere.py에서 import한 함수이다.

### crawler_Youtube.py

- [x] get_yt_video_id(url): 유튜브 url을 입력했을 때 query를 속에 있는 video의 id를 뽑아내준다. 
  - 함수 자체 기능
    - youtube의 url은 종류가 여러 가지이기 때문에, url의 종류에 따라서 video id를 뽑는 방식을 설정했다. 	
  - 의존하는 기능: 모듈 urllib3의 함수 urlparse와 parse_qs
    - 주의사항: python3에서 쓰이는 urllib는 python2.7 urllib과는 다름을 유의하자. "from urllib.parse import urlparse, parse_qs"으로 작성해야 제대로 모듈을 import할 수 있다. 

- [x] ytbe_cmt_rply(video_url): YouTube API를 통해서 비디오 URL을 입력했을 때 해당 URL에 달린 커멘트들의 갯수를 no_of_comments로 반환한다. 
  - 함수 자체 기능
    - googleapiclient를 통해서 commentThreads()에 request를 한다. 
  - 의존하는 기능
    - 동일한 python 파일에서 정의한 함수 get_yt_video_id(url)
    - googleapiclient: googleapiclient로 youtube url에 달린 커멘트들의 갯수를 구한다. 사용하는 것은 YouTube API이며, googleapiclient는 YouTube API에 접근할 수 있게하는 모듈이다. api_service_name, api version, developer_key를 먼저 정의해야 YouTube API를 사용할 수 있다. 

