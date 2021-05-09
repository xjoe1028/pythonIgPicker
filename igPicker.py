from pyquery import PyQuery as pq
import json
from flask import Flask
import requests
import time
import random

# TODO:以後改成restfulApi 從前端取得文章網址 https://www.instagram.com/p/COnWWSuHB6l/
article_url = 'https://www.instagram.com/p/CNWeZdNMIt7/'

# 取出 文章網址的後面shortCode ex: /p/COnWWSuHB6l/
articleShortCode = article_url[25:]
print('articleShortCode = ' + articleShortCode)

# 每次加載留言送出request url
request_url = 'https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables=%7B%22shortcode%22%3A%22{short_code}%22%2C%22first%22%3A12%2C%22after%22%3A%22%7B%5C%22cached_comments_cursor%5C%22%3A+%5C%22{cached_comments_cursor}%5C%22%2C+%5C%22bifilter_token%5C%22%3A+%5C%22{bifilter_token}%5C%22%7D%22%7D'

# 抓留言要有登錄的cookie
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'cookie': 'ig_did=B005B2B6-7310-4BEF-B463-18345221B916; mid=X31WiQALAAFlNzHcemjPLj_80daX; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; shbid=12681; shbts=1617844570.5476303; rur=VLL; fbsr_124024574287414=5aqF_3oRUOlqyvMe_81hRLo7iqkiH-DmguCAT2vHxTE.eyJ1c2VyX2lkIjoiMTAwMDAwNTAxODUzMzE3IiwiY29kZSI6IkFRQzJBLXlhendmR242NVc2VW9ZblZiSGFFQ1NEa0pvR1FFYl92bndldVFSRHFwSHI5ZE9ONmFLOHZCSmRkNnozT2pLcEtVcF9pb3NUazhLTHpsSE50Qk5jRkZscFdXaEk0Y1Y1NFVTbVhDWXlfVlZrSHhwdzhScHFFbjRNUzEtd0NJTGhpcUIwaUE1LWJ2akh0al9ybEVvalJTd3NtbkxNRGdYbldXSzluS1ZMSHpJZGZYaWpaUi1FVkstY0hhVDI0QU95YWwxZk5nM3MxZDJQaUpQRVg2YmVFdHpmTFNFRGc5VWRGR0N6QjB4bG11TlVvelphX0VLR1JNbjhTQ1gwdlMwZFdwem12N3ZxSmZxUlhDNVpxU3V0a2tON2w3bWwyVGtBTjhqeXJIZUc4aDhnRFFWYTZCaXNvZ0JUMVJpeFFVSWFfTHNkbTRyNFNPUWRla0kxQnVrUzhVTmxXeUUzakMtSGgyblhBa2Q3dyIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQkFDSmFQZkdVeW40Y1dTdjlQcXB3ZU5FdG9YVHJDV2lJYVl4WkI1SHh3ZmVaQzFVcURVYk9yQ3lGaURHenhrWkFQUjh5VmxvRE5Gbmd5T0ltZDJESkdyS1g1OGhQdTlEcjRaQlkyNW1xNnJGVWNLMHhhVWZ4azBxTzhqdWFGSTE2aGlhUmxNY3YzaEswN3ZtQVROZjJsdUR0Yzl6SnJQN0pYWkM5UjBSSE4iLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYxNzkzOTYyMX0; csrftoken=oTtMk9D9bzpanOcLvDgA1EAtKAJ5TuMz; ds_user_id=303222200; sessionid=303222200%3AgLRXg9BazrbE3M%3A14; fbsr_124024574287414=5aqF_3oRUOlqyvMe_81hRLo7iqkiH-DmguCAT2vHxTE.eyJ1c2VyX2lkIjoiMTAwMDAwNTAxODUzMzE3IiwiY29kZSI6IkFRQzJBLXlhendmR242NVc2VW9ZblZiSGFFQ1NEa0pvR1FFYl92bndldVFSRHFwSHI5ZE9ONmFLOHZCSmRkNnozT2pLcEtVcF9pb3NUazhLTHpsSE50Qk5jRkZscFdXaEk0Y1Y1NFVTbVhDWXlfVlZrSHhwdzhScHFFbjRNUzEtd0NJTGhpcUIwaUE1LWJ2akh0al9ybEVvalJTd3NtbkxNRGdYbldXSzluS1ZMSHpJZGZYaWpaUi1FVkstY0hhVDI0QU95YWwxZk5nM3MxZDJQaUpQRVg2YmVFdHpmTFNFRGc5VWRGR0N6QjB4bG11TlVvelphX0VLR1JNbjhTQ1gwdlMwZFdwem12N3ZxSmZxUlhDNVpxU3V0a2tON2w3bWwyVGtBTjhqeXJIZUc4aDhnRFFWYTZCaXNvZ0JUMVJpeFFVSWFfTHNkbTRyNFNPUWRla0kxQnVrUzhVTmxXeUUzakMtSGgyblhBa2Q3dyIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQkFDSmFQZkdVeW40Y1dTdjlQcXB3ZU5FdG9YVHJDV2lJYVl4WkI1SHh3ZmVaQzFVcURVYk9yQ3lGaURHenhrWkFQUjh5VmxvRE5Gbmd5T0ltZDJESkdyS1g1OGhQdTlEcjRaQlkyNW1xNnJGVWNLMHhhVWZ4azBxTzhqdWFGSTE2aGlhUmxNY3YzaEswN3ZtQVROZjJsdUR0Yzl6SnJQN0pYWkM5UjBSSE4iLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYxNzkzOTYyMX0'
}


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('請求錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        return None


def get_json(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('請求網頁json錯誤, 錯誤狀態碼：', response.status_code)
    except Exception as e:
        print(e)
        time.sleep(60 + float(random.randint(1, 4000))/100)
        return get_json(url)


def getAllcomments(url):
    commentsList = []
    doc = pq(html)
    items = doc('script[type="text/javascript"]').items()

    for item in items:
        # 未登錄時全部放在 window._sharedData 登錄時放在 window.__additionalDataLoaded
        # window.__additionalDataLoaded('/p/CNWeZdNMIt7/'
        searchStr = "window.__additionalDataLoaded('" + articleShortCode + "'"
        # print('searchStr = ' + searchStr)
        if item.text().strip().startswith(searchStr):
            # print(item.text()[48:-2])
            js_data = json.loads(item.text()[48:-2], encoding='utf-8')
            print(js_data)
            # edges = js_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"] 包著所有單篇文章留言所有資訊的最外層
            # edge_media_to_caption 文章
            edge_caption = js_data["graphql"]["shortcode_media"]["edge_media_to_caption"]
            # 發文者資訊
            owner = js_data["graphql"]["shortcode_media"]["owner"]
            # edge_media_to_parent_comment 留言
            edge_parent_comment = js_data["graphql"]["shortcode_media"]["edge_media_to_parent_comment"]

            # https://www.instagram.com/p/CNWeZdNMIt7/ 後面的CNWeZdNMIt7就是shortcode
            short_code = js_data["graphql"]["shortcode_media"]["shortcode"]

            # 判斷有無加載留言的物件
            page_info = edge_parent_comment["page_info"]
            # 下一條XHR請求的url裡的after參數的值 TODO: 當留言少於12則 就為null
            end_cursor = page_info["end_cursor"]
            # 該url是否是最后一條url的布林值 TODO: 當留言少於12則 直接為false
            has_next_page = page_info["has_next_page"]
            print('shortcode = ' + short_code)
            print('end_cursor = ' + end_cursor)
            end_cursor_to_json = json.loads(end_cursor, encoding='utf-8')
            # 有登錄 要加載留言requst需要的request參數
            cached_comments_cursor = end_cursor_to_json["cached_comments_cursor"]
            bifilter_token = end_cursor_to_json["bifilter_token"].replace(
                '=', '%3D')
            # tao_cursor = end_cursor_to_json["end_cursor_to_json"].replace(
            #     '=', '%3D')
            print('cached_comments_cursor = ' + cached_comments_cursor)
            print('bifilter_token = ' + bifilter_token)
            # print('tao_cursor = ' + tao_cursor)
            print("-----------------------------------------------------------印出edge_caption文章的物件-----------------------------------------")
            article = edge_caption["edges"][0]["node"]["text"]
            author_account = owner["username"]
            author = owner["full_name"]
            author_id = owner["id"]
            print("發文者：" + author)
            print("發文者帳號：" + author_account)
            print("發文者id：" + author_id)
            print("文章內容：" + article.replace('\n', ''))
            print("-----------------------------------------------------------印出edge_parent_comment留言的物件-----------------------------------------")
            comments_total = str(edge_parent_comment["count"])  # 將留言總數int轉str
            print("總留言數：" + comments_total + "筆")
            print("-----------------------------------------------------------印出每則留言----------------------------------------------")

            edge_comments = edge_parent_comment["edges"]  # 留言的List
            i = 1
            for edge_comment in edge_comments:
                # 留言內容
                comment = edge_comment["node"]["text"].replace('\n', '')
                # 帳號
                username = edge_comment["node"]["owner"]["username"]
                print("第" + str(i) + "則留言")
                print("留言帳號：" + username)
                print("留言內容：" + comment)
                print("----------------------------------------------------------------------------------------------------------------------")
                if i < len(edge_comments):
                    i += 1
                comment_object = {}
                comment_object["username"] = username
                comment_object["comment"] = comment
                commentsList.append(comment_object)
            print("總共" + str(i) + "則")
            print("還剩" + str(edge_parent_comment["count"] - i) + "則")

            # TODO: ajax動態加載留言
            i += 1
            while has_next_page:
                # 判斷 cached_comments_cursor 不為none時 送出的請求 會有所不同
                # if cached_comments_cursor is not None:
                uri = request_url.format(
                    short_code=short_code, cached_comments_cursor=cached_comments_cursor, bifilter_token=bifilter_token
                )
                # else if cached_comments_cursor is None & tao_cursor is None:
                #     uri = request_url.format(
                #         short_code=short_code, bifilter_token=bifilter_token
                #     )
                # else:
                #     uri = request_url.format(
                #         short_code=short_code, bifilter_token=bifilter_token, tao_cursor=tao_cursor
                #     )
                print('uri = ' + uri)
                js_data = get_json(uri)
                # print("-------js_data--------")
                # print(js_data)

                edge_parent_comment = js_data["data"]["shortcode_media"]["edge_media_to_parent_comment"]
                # 判斷有無加載留言的物件
                page_info = edge_parent_comment["page_info"]
                # 下一條XHR請求的url裡的after參數的值
                end_cursor = page_info["end_cursor"]
                print('end_cursor = ' + end_cursor)
                # 該url是否是最後一條url的布林值
                has_next_page = page_info["has_next_page"]
                # 有登錄 加載留言requstUrl需要的request參數
                end_cursor_to_json = json.loads(end_cursor, encoding='utf-8')
                cached_comments_cursor = end_cursor_to_json["cached_comments_cursor"]
                bifilter_token = end_cursor_to_json["bifilter_token"].replace(
                    '=', '%3D')
                print('cached_comments_cursor = ' + cached_comments_cursor)
                print('bifilter_token = ' + bifilter_token)
                print("-----------------------加載的留言--------------------------")
                # 留言內容
                edge_comments = edge_parent_comment["edges"]
                j = 1
                for edge_comment in edge_comments:
                    comment = edge_comment["node"]["text"].replace('\n', '')
                    username = edge_comment["node"]["owner"]["username"]
                    print("第" + str(i) + "則留言")
                    print("留言帳號：" + username)
                    print("留言內容：" + comment)
                    print("------------------------------------------------------")
                    ajaxCommentObject = {}
                    ajaxCommentObject["username"] = username
                    ajaxCommentObject["comment"] = comment
                    commentsList.append(ajaxCommentObject)
                    if j < len(edge_comments):
                        j += 1
                        i += 1
                print("一次加載" + str(j) + "則")
                print("總共加載" + str(i) + "則")
                print("還剩" + str(edge_parent_comment["count"] - i) + "則")

    return commentsList


class checkJSON(object):
    # 取得Json物件所有key
    def getJsonAllKey(self, data):
        keysAll_list = []

        def getKeys(data):  # 遍厲json所有key
            if (type(data) == type({})):
                keys = data.keys()
                for key in keys:
                    value = data.get(key)
                    if (type(value) != type({}) and type(value) != type([])):
                        keysAll_list.append(key)
                    elif (type(value) == type({})):
                        keysAll_list.append(key)
                        getKeys(value)
                    elif (type(value) == type([])):
                        keysAll_list.append(key)
                        for para in value:
                            if (type(para) == type({}) or type(para) == type([])):
                                getKeys(para)
                            else:
                                keysAll_list.append(para)
        getKeys(data)
        return keysAll_list

    # 檢查Json物件裡面是否有此key
    def checkJsonKey(self, data, tagKey):
        if(type(data) != type({})):
            print("此json物件為空物件!!")
        else:
            key_list = self.getKeys(data)
            for key in key_list:
                if(key == tagkey):
                    return True
        return False


#  Test成功
# cjson = checkJSON()
# testData = {"a": 1, "ss": 2, "test": '00033'}
# list = cjson.getJsonAllKey(testData)
# print(list)

html = get_html(article_url)
allComments = getAllcomments(html)
print(allComments)
