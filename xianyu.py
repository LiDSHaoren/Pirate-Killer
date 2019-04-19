
import csv
import requests
import time
import urllib
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from wxpy import *

bot = Bot(cache_path=True)

accept_text = "加好友"
invite_text = "我是盗版杀手机器人，请通过回复配置你的信息\n第一步：配置闲鱼搜索的关键词，从而定位盗版商品\n\n请按格式回复你的配置信息，格式如下\n'搜索关键词 您的内容'\n示例：\n搜索关键词 麻瓜编程、自动办公、实用主义学Python"
config_text_1 = "你配置的信息如下："
config_text_2 = "搜索关键词"
config_text_3 = "确认请回复1"
config_text_4 = "如需修改请回复2"
config_text_5 = "盗版"
config_text_6 = "请修改您的配置信息"

def plea(data ="麻瓜编程"):
    q = urllib.parse.quote(data, encoding="gbk") # 转化为url 读取的语言
    url = f"https://s.2.taobao.com/list/?q={q}&search_type=item&app=shopsearch"
    print(url)
    ua = UserAgent(verify_ssl=False)
    headers = {"User-Agent":ua.random,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
    r = requests.get(url,headers = headers)
    return r.text

def analy(msg,key):
    t1 = time.time()
    file_name = f"{msg.sender.nick_name}&{key}.csv"
    new_file = open(file_name,"w",newline="")
    writer = csv.writer(new_file)
    header = ["title","href"] # 标题
    writer.writerow(header)
    r = plea(key)
    soup = BeautifulSoup(r,"html.parser")
    pirate_count_sel = "#J_ItemListsContainer > div > div > div > dl > dd > div > span > em"
    pirate_name_sel = "div > div > div.item-seller > div.seller-avatar > a"
    pirate_link_sel = "div > div > div.item-info > div.item-pic > a"
    pirate_count = soup.select(pirate_count_sel)[0].get_text()
    count_msg = f"闲鱼上共有{pirate_count}条信息，请及时处理"
    print(count_msg)
    msg.sender.send(count_msg)
    names = soup.select(pirate_name_sel)
    links = soup.select(pirate_link_sel)
    for name,link in zip(names,links):
        file = []
        file.append(name.get("title"))
        file.append(link.get("href"))
        writer.writerow(file)
        msg.sender.send(name.get("title"))
        msg.sender.send(link.get("href"))
        time.sleep(1)
    print(f"仅显示{len(links)}信息，请及时处理")
    t = time.time()- t1
    new_file.close()
    msg.sender.send_file(file_name,media_id=True)
    print(f"{float('%.2f' % t)}s,Done!")
    msg.sender.send(f"{float('%.2f' % t)}s,Done!")

# 第一步 加好友 注册的是加好友的消息
def main():
    @bot.register(msg_types = FRIENDS)
    def auto_accept_friends(msg):
        if accept_text in msg.text.lower():
            # 接受好友 (msg.card 为该请求的用户对象)
            new_friend = bot.accept_friend(msg.card)
            new_friend.send(invite_text)

    # 找到回复对应msg的人
    @bot.register(Friend,TEXT)
    def config_msg(msg):
        if config_text_5 == msg.text.lower():
            msg.sender.send(invite_text)
        elif config_text_2 in msg.text.lower():
            msg.sender.send(config_text_1)
            msg.sender.send(config_text_2 + msg.text.split(config_text_2)[-1])
            msg.sender.send(config_text_3)
            msg.sender.send(config_text_4)
        elif "1" in msg.text.lower():
            history = bot.messages.search("关键词",sender = msg.sender)
            if len(history) == 0:
                msg.send("机器人无法找到你的配置信息，请重新配置")
            else:
                msg.sender.send("正在处理中，请稍后")
                print(history)
                key = history[-1].text.split("搜索关键词")[-1]
                print(key)
                analy(msg,key)
        elif "2" in msg.text.lower():
            msg.sender.send("请重新配置信息")
        else:
            pass

    # @bot.register(my_group, msg_types=TEXT)
    # def group(msg):
    #     # if msg.is_at:
    #     tuling.do_reply(msg)
    #     # else:
    #     #     pass
    bot.join()      

if __name__ == '__main__':
    main()
