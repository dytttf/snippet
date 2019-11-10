# coding:utf8
"""
博客园
    https://www.cnblogs.com/#p4
    首页前200页文章列表信息采集
"""
import re
import os
import json
import time
import requests
from bs4 import BeautifulSoup


def download(page):
    url = "https://www.cnblogs.com/AggSite/AggSitePostList"
    data = {
        "CategoryType": "SiteHome",
        "ParentCategoryId": 0,
        "CategoryId": 808,
        "PageIndex": page,
        "TotalPostCount": 4000,
        "ItemListActionName": "AggSitePostList",
    }
    headers = {
        "accept": "text/plain, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://www.cnblogs.com",
        "pragma": "no-cache",
        "referer": "https://www.cnblogs.com/",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }
    r = requests.post(url, headers=headers, json=data)
    return r


def parse(response):
    soup = BeautifulSoup(response.text, "lxml")
    data_list = []
    for item in soup.select("div.post_item"):
        data = {
            "url": item.select_one("a.titlelnk").attrs["href"],
            "title": item.select_one("a.titlelnk").text.strip(),
            "summary": item.select_one("p.post_item_summary").text.strip(),
            "author": item.select_one("a.lightblue").text.strip(),
            "author_url": item.select_one("a.lightblue").attrs["href"],
            "ctime": re.search("发布于\s*(\d+-\d+-\d+ \d+:\d+)", str(item)).group(1),
        }
        data_list.append(data)
    return data_list


def main():
    """
    https://www.cnblogs.com/#p4
    :return:
    """
    data_file = "cnblogs_blog.json"
    # 加载本地数据
    if os.path.exists(data_file):
        try:
            data_dict = json.load(open(data_file, encoding="utf8"))
        except:
            data_dict = {}
    else:
        data_dict = {}
    try:
        for page in range(1, 201):
            r = download(page)
            time.sleep(2)
            #
            for data in parse(r):
                data_dict[data["url"]] = data
            print("当前页码: {}  总数据量: {}".format(page, len(data_dict)))
    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        with open(data_file, "w", encoding="utf8") as f:
            json.dump(data_dict, f, ensure_ascii=False)

    return


if __name__ == "__main__":
    main()
