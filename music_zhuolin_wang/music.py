# coding:utf8
"""
http://music.zhuolin.wang/
音乐下载
"""
import os
import json
import time
import random
import requests

cur_path = os.path.dirname(os.path.abspath(__file__))


class ZhuoLinMusic(object):
    def __init__(self, mp3_dir: str = ""):

        # 下载目录
        self.mp3_dir = mp3_dir
        if not self.mp3_dir:
            self.mp3_dir = os.path.join(cur_path, "mp3")

        if not os.path.exists(self.mp3_dir):
            os.makedirs(self.mp3_dir, exist_ok=True)

    def download(self, url, method="GET", **kwargs):
        """下载器"""
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "music.zhuolin.wang",
            "Origin": "http://music.zhuolin.wang",
            "Referer": "http://music.zhuolin.wang/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        response = requests.request(method, url, **kwargs)
        return response

    def download_by_music_id(self, music_id: str, source: str = "netease"):
        """
        下载音乐
        :param music_id:
        :param source:
        :return:
        """
        # 获取mp3地址
        url = "http://music.zhuolin.wang/api.php?callback={}".format(self.make_callback())
        data = {
            "types": "url",
            "id": music_id,
            "source": source,
        }
        headers = {
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Content-Length": "25",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }
        response = self.download(url, method="POST", data=data, headers=headers)
        l, r = response.text.find("{"), response.text.rfind("}")
        j_response = json.loads(response.text[l:r + 1])
        mp3_url = j_response['url']
        # 下载mp3
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        mp3_response = self.download(mp3_url, headers=headers)
        return mp3_response

    def download_playlist(self, playlist_id: str = "3778678"):
        """
        下载播放列表中全部歌曲
        :param playlist_id:
            云音乐热歌榜 3778678  默认显示这个
            云音乐新歌榜 3779629
        :return:
        """
        # 获取播放列表
        play_list = self.get_playlist(playlist_id=playlist_id)
        for item in play_list:
            # 构造唯一标识符
            unique_name = self.make_unique_name(item)
            # 不重复下载
            # 卧槽 还有重名的
            mp3_file_name = os.path.join(self.mp3_dir, "{}.mp3".format(unique_name))
            if not os.path.isfile(mp3_file_name):
                print("开始下载: {} ...".format(unique_name))
                mp3_response = self.download_by_music_id(item["id"])
                with open(mp3_file_name, "wb") as f:
                    f.write(mp3_response.content)
                time.sleep(2)
            else:
                print("跳过已下载歌曲: {}".format(unique_name))
        return

    def get_playlist(self, playlist_id: str = "3778678") -> list:
        """
        获取播放列表
        callback 生成:
            l = "1.11.3"  版本号
            "jQuery" + (l + Math.random()).replace(/\D/g, "")

        参数:
            types:  应该都是 playlist
            id: 区分不同的播放列表
                摘抄几个:
                    云音乐热歌榜 3778678  默认显示这个
                    云音乐新歌榜 3779629
        :param playlist_id:
        :return:
        """
        url = "http://music.zhuolin.wang/api.php?callback={}".format(self.make_callback())
        data = {
            "types": "playlist",
            "id": playlist_id,
        }
        headers = {
            "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
            "Content-Length": "25",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }
        response = self.download(url, method="POST", data=data, headers=headers)
        l, r = response.text.find("{"), response.text.rfind("}")
        j_response = json.loads(response.text[l:r + 1])
        # 获取播放列表
        play_list = []
        tracks = j_response["playlist"]['tracks']
        return tracks

    def make_callback(self):
        return "jQuery1113{}_{}".format(str(random.random()).replace("0.", ""), int(time.time() * 10))

    def make_unique_name(self, item):
        """
        构造歌曲唯一名称 暂定
            名字_歌手_专辑
        :param item:
        :return:
        """
        name = item["name"]
        singer = item["ar"][0]["name"] if item["ar"] else ""
        album = item["al"]["name"] if item["al"] else ""
        return "{}_{}_{}".format(name, singer, album)


if __name__ == "__main__":
    zm = ZhuoLinMusic()
    zm.download_playlist()
