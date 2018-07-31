#coding=utf8
import os
import pprint
import re
from collections import OrderedDict

import requests
import urllib3
from bs4 import BeautifulSoup

baseUrl = "https://www.douyu.com/"

pp = pprint.PrettyPrinter(indent=4)  # 格式化输出字典


# 获取所有直播项目
class Douyu:
    def __init__(self):
        self.__url = baseUrl + "directory/"  #之后修改在配置文件里
        self.__directoryList = []
        self.__games = []
        self.__lives = []

    def get_directoryList(self):
        r = requests.get(self.__url, verify=False)  # verify=False在打开https网页时使用
        content = r.content

        # 使用bs4格式化获取的网页
        soup = BeautifulSoup(content, "lxml")
        live_list = soup.find("div", {
            "class": "info"
        }).find_all(
            "a", attrs={"data-cid": True})

        num = 0
        for i in live_list:
            directory = {}
            name = re.sub('\s', "", i.string)  # 正则删除空格
            location = i['data-href']  # 跳转地址
            directory["dir_id"] = num
            directory["dir_name"] = name
            directory["dir_url"] = location
            self.__directoryList.append(directory)
            num += 1

        # pp.pprint(self.__directoryList)
        print("所有分类：")
        # 下面也是重复使用的代码，封装一下
        for i in self.__directoryList:
            pp.pprint("[" + str(i["dir_id"]) + "]" + i["dir_name"])
        tmp = input("请选择数字：")
        if tmp.isdigit() and (0 <= eval(tmp) <= len(
                self.__directoryList)):  # isdigit()判断每个字符都是数字
            for i in self.__directoryList:
                if i["dir_id"] == eval(tmp):
                    # pp.pprint(i["dir_url"])
                    return i["dir_url"]
                continue
        elif not tmp.isdigit():
            pp.pprint("输入类型有误！")
        else:
            pp.pprint("输入范围有误！")

    def get_games(self):
        location = self.get_directoryList()

        url = baseUrl + location

        r = requests.get(url, verify=False)
        content = r.content
        soup = BeautifulSoup(content, "lxml")  # 这三行应该封装一下

        live_list = soup.find("ul", {
            "id": "live-list-contentbox"
        }).find_all("li", {"class": "unit"})
        num = 0
        for i in live_list:
            game = {}
            name = i.find("p").string
            location = i.find("a", attrs={"data-tid": True})['href']
            game["game_id"] = num
            game["game_name"] = name
            game["game_url"] = location
            self.__games.append(game)
            num += 1

        # pp.pprint(self.__games)
        print("所有游戏：")
        for i in self.__games:
            pp.pprint("[" + str(i["game_id"]) + "]" + i["game_name"])
        tmp = input("请选择数字：")
        if tmp.isdigit() and (0 <= eval(tmp) <= len(
                self.__games)):  # isdigit()判断每个字符都是数字
            for i in self.__games:
                if i["game_id"] == eval(tmp):
                    # pp.pprint(i["game_url"])
                    return i["game_url"]
                continue
        elif not tmp.isdigit():
            pp.pprint("输入类型有误！")
        else:
            pp.pprint("输入范围有误！")

    def get_live(self):
        location = self.get_games()

        url = baseUrl + location

        r = requests.get(url, verify=False)
        content = r.content
        soup = BeautifulSoup(content, "lxml")  # 这三行应该封装一下

        live_list = soup.find("ul", {
            "id": "live-list-contentbox"
        }).find_all("li")

        num = 0
        for i in live_list:
            live = {}
            streamer = i.find("span", {"class": "dy-name"}).string
            title = i.find("a")['title']
            location = i.find("a")['href']
            live["live_id"] = num
            live["live_streamer"] = streamer
            live["live_title"] = title
            live["live_url"] = location
            self.__lives.append(live)
            num += 1

        # pp.pprint(self.__lives)
        print("所有直播：")
        for i in self.__lives:
            pp.pprint("[" + str(i["live_id"]) + "]" + i["live_streamer"] +
                      " : " + i["live_title"])
        tmp = input("请选择数字：")
        if tmp.isdigit() and (0 <= eval(tmp) <= len(
                self.__lives)):  # isdigit()判断每个字符都是数字
            for i in self.__lives:
                if i["live_id"] == eval(tmp):
                    # pp.pprint(i["live_url"])
                    return i["live_url"]
                continue
        elif not tmp.isdigit():
            pp.pprint("输入类型有误！")
        else:
            pp.pprint("输入范围有误！")

    def live_run(self):
        location = self.get_live()

        url = baseUrl + location

        os.system("you-get -p vlc " + url)


if __name__ == "__main__":
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    start = Douyu()
    # start.get_games(directoryList)
    start.live_run()
