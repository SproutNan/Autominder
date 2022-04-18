from nonebot import get_driver
import random
import math
import os
from datetime import date
import time
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from .config import Config
import pygame
import os
import pandas as pd
import re

pygame.init()

global_config = get_driver().config
config = Config.parse_obj(global_config)


def luck_simple(num):
    if num < 81:
        return '菜'
    else:
        return '一般般，比我菜点'


def jrrp_return(num):
    if num < 14:
        return '凶'
    elif num < 28:
        return '小吉'
    elif num < 50:
        return '半吉'
    elif num < 90:
        return '吉'
    else:
        return '大吉'


def chouka_return(a, ys_list):
    if a < 3:
        return ys_list[3]
    elif a < 6:
        return ys_list[2]
    elif a < 10:
        return ys_list[1]
    else:
        return ys_list[0]
    

gpa = on_keyword(['ycgpa','预测GPA'],priority=50)
@gpa.handle()
async def gpa_handle(bot: Bot, event: Event):
    #if str(event.json()).count("662368872") == 0:
        #await gpa.finish()
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    lucknum = rnd.randint(1,100) / 100 * 4.3
    await gpa.finish(Message(f'[CQ:at,qq={event.get_user_id()}]您下一门课GPA最有可能是{int(lucknum)}.{rnd.randint(1,9)}，{luck_simple(lucknum/4.3*100)}'))

jrrp1 = on_keyword(['率：'],priority=50)
@jrrp1.handle()
async def jrrp1_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word[0:len("率：")] != "率：":
        await jrrp1.finish()
      
    slice_ = word[word.find('率：')+len('率：'):]
    #if str(event.json()).count("662368872") == 0:
        #await jrrp1.finish()
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()) ** 4 + hash(slice_))
    lucknum = rnd.randint(0, 100)
    await jrrp1.finish(Message(f'[CQ:at,qq={event.get_user_id()}] 您今天的{slice_}率为{int(lucknum)}%'))

battle = on_keyword(['battle','battle with'],priority=47)
@battle.handle()
async def battle_handle(bot: Bot, event: Event):
    #if str(event.json()).count("662368872") == 0:
        #await battle.finish()
    msg = str(event.get_message())
    sb = str(event.raw_message)
    start = sb.find("qq=")
    if start == -1:
        await battle.finish()
        
    end = sb.find("]")
    player = sb[start+3:end]

    if (player == '2630128240' or event.get_user_id() == 2630128240 or player == str(event.get_user_id())):
        await battle.finish()

    rnd1 = random.Random().randint(12, 99)
    rnd2 = random.Random().randint(12, 99)

    
    player1 = player
    player2 = event.get_user_id()
    win = ""
    lose = ""
    if rnd1 > rnd2:
        win = player1
        lose = player2
    elif rnd1 <= rnd2:
        win = player2
        lose = player1
    await battle.finish(Message(f'打杜宝挑战！对手打了{rnd1}下，[CQ:at,qq={player2}]打了{rnd2}下，[CQ:at,qq={win}]获胜！'))

choice1 = on_keyword(['选：'], priority=46)
@choice1.handle()
async def choice1_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word[0:len("选：")] != "选：":
        await choice1.finish()
        
    slice_ = list(set(word[word.find('选：')+len('选：'):].split()))
  
    if len(slice_) > 1:
        await choice1.finish(Message(f'回应是：{random.choice(slice_)}'))
    else:
        await choice1.finish()

choice = on_keyword(['sudo 选：'], priority=46)
@choice.handle()
async def choice_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    slice_ = list(set(word[word.find('sudo 选：')+len('sudo 选：'):].split()))
    ans = random.choice(slice_)
    cnt = 1
    for _ in range(99):
        if random.choice(slice_) == ans:
            cnt+=1
            
    if len(slice_) > 1 and len(slice_) < 11:
        await choice.finish(Message(f'回应是：{random.choice(slice_)}，{cnt}/100'))
    else:
        await choice.finish()

add_fungi = on_keyword(['起名：'], priority=46)
@add_fungi.handle()
async def add_fungi_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    name = word[word.find('起名：')+len('起名：'):]
    if len(name) > 20:
        await add_fungi.finish(Message(f'名字太长了！'))
    path = "C:/bot_things/namemap/"
    path += event.get_user_id()
    data = open(path, "w")
    data.write(name)
    data.close()
    await add_fungi.finish(Message(f'你好呀，{name}'))

move = on_keyword(['移动到：'], priority=46)
@move.handle()
async def move_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    name = word[word.find('移动到：')+len('移动到：'):]
    path = "C:/bot_things/location/"
    path += event.get_user_id()
    data = open(path, "w")
    data.write(name)
    data.close()
    await move.finish(Message(f'你已经移动到{name}！'))

def getNameById(id_):
    path = "C:/bot_things/namemap/"
    namelist = os.listdir(path)
    if id_ not in namelist:
        return id_
    path += id_
    return open(path).read()

here = on_keyword(['当前位置'], priority=46)
@here.handle()
async def here_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "当前位置":
        await here.finish()

    path = "C:/bot_things/location/"
    id_ = event.get_user_id()
    yourpath = path + id_
    data = open(yourpath).read()

    mess = "你当前在"
    mess += data

    friends = []
    listmap = os.listdir(path)
    for _ in listmap:
        inner = open(path+_).read()
        if inner == data and _ != id_:
            friends.append(_)

    if len(friends):
        mess += "，当前在这里的朋友还有："
        for i in friends:
            mess += getNameById(i)
            mess += ", "
        mess = mess[:len(mess)-2]
    mess += "。"
    await here.finish(Message(f'{mess}'))

lookmap = on_keyword(['世界'], priority=48)
@lookmap.handle()
async def lookmap_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "世界":
        await lookmap.finish()

    mess = ""
    path = "C:/bot_things/location/"
    listmap = os.listdir(path)
    for _ in listmap:
        mess += getNameById(_)
        mess += "在"
        mess += open(path+_).read()
        mess += "\n"

    mess = mess[:len(mess)-1]
    await lookmap.finish(Message(f'{mess}'))

def getCardEffect(s):
    return hash(s) % 5 + 10 * (hash(s) % 100)

def getCardValue(s):
    return chouka_return(hash(s) % 100, ['[N] ', '[R] ', '[SR] ', "[SSR] "])

chouka = on_keyword(['抽卡'], priority=48)
@chouka.handle()
async def chouka_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "抽卡":
        await chouka.finish()

    id_ = event.get_user_id()
    name = ["群主", "66", "蟹老板", "sjj", "顾炎武", "大姐", "美丽学妹珍珠棉", "陈日天", "杜宝", "酚酞女", "原批", "樱桃", "柳杭羽", "程心", "花如雪", "尧尧", "方火华", "lkz", "王梓媛", "gjj"]
    prefix = ["攀岩的", "喝奶茶的", "拍视频的", "打羽毛球的", "踢足球的", "想发paper的", "想染头发的", "好厉害的", "无敌的", "水群的", "flxg的", "吃夜宵的", "做推送的", "菜的", "在报销的", "谈恋爱的", "直播的", "摸鱼的", "躺平的", "内卷的"]
    
    his_time = open("C:/bot_things/carddue").read()
    his = eval(his_time)

    cd = 86400
    flag = False #是否允许抽卡
    if his.get(id_, default=None) is None:
        flag = True
    elif int(time.time()) - int(his.get(id_)) > cd:
        flag = True

    if flag:
        # 更新时间
        his[id_] = str(int(time.time()))
        save_time = open("C:/bot_things/carddue", "w+")
        save_time.write(his.__repr__())

        # 抽一张卡
        choice = random.choice(prefix)+random.choice(name)

        # 打开背包
        data = open("C:/bot_things/cardbackpack/"+id_, "a+")
        data.seek(0)
        data2 = data.read()
        if len(data2):
            back = eval(data2)
        else:
            back = []

        # 更新背包
        if choice in back:
            await chouka.finish(Message(f'{getNameById(id_)}抽到了已有卡牌{getCardValue(choice)}+{choice}。'))

        back.append(choice)
        data = open("C:/bot_things/cardbackpack/"+id_, "w+")
        data.write(back.__repr__())
        await chouka.finish(Message(f'{getNameById(id_)}抽到了新卡{getCardValue(choice)}+{choice}！'))

    else:
        await chouka.finish(Message(f'{(int(his.get(id_)) + cd + 1 - int(time.time()))}s后才可再次抽卡！'))

chupai = on_keyword(['出牌'], priority=48)
@chupai.handle()
async def chupai_handle(bot: Bot, event: Event):
    id_ = event.get_user_id()
    word = str(event.raw_message)
    matchobj = re.match("出牌 (.*) (.*)", word, re.M|re.I)
    if matchobj is None: # 回血
        matchobj = re.match("出牌 (.*)", word, re.M | re.I)
        if matchobj is None:
            await chupai.finish()
            cardNum = matchobj.group(1)
            if cardNum.isdecimal() is False:
                await chupai.finish()
            # 打开背包
            data = open("C:/bot_things/cardbackpack/" + id_, "a+")
            data.seek(0)
            data2 = data.read()
            if len(data2):
                back = eval(data2)
            else:
                back = []

            if len(back) < int(cardNum):
                await chupai.finish(Message(f'你没有第{cardNum}张牌！'))
            # 删除卡片
            cardname = back[cardNum - 1]
            back.remove(back[cardNum - 1])
            data = open("C:/bot_things/cardbackpack/" + id_, "w+")
            data.write(back.__repr__())

            # 记录攻击
            data = open("C:/bot_things/cardeffect").read()
            data = eval(data)
            data[id_] = str(int(data.get(id_, default="0")) + getCardEffect(cardname))
            data2 = open("C:/bot_things/cardeffect", "w+")
            data2.write(data.__repr__())

            # 返回值
            await chupai.finish(Message(f'{getNameById(id_)}恢复了{getCardEffect(cardname)}点血量！'))

    cardNum = matchobj.group(1)
    atSb = matchobj.group(2)
    if cardNum.isdecimal() is False or re.match("CQ:at,qq=(.*)", atSb, re.M|re.I) is None:
        await chupai.finish()
    # 获得命令

    # 打开背包
    data = open("C:/bot_things/cardbackpack/" + id_, "a+")
    data.seek(0)
    data2 = data.read()
    if len(data2):
        back = eval(data2)
    else:
        back = []

    if len(back) < int(cardNum):
        await chupai.finish(Message(f'你没有第{cardNum}张牌！'))
    # 删除卡片
    cardname = back[cardNum-1]
    back.remove(back[cardNum-1])
    data = open("C:/bot_things/cardbackpack/" + id_, "w+")
    data.write(back.__repr__())

    # 记录攻击
    data = open("C:/bot_things/cardeffect").read()
    data = eval(data)
    data[atSb] = str(int(data.get(atSb, default="0")) - getCardEffect(cardname))
    data2 = open("C:/bot_things/cardeffect", "w+")
    data2.write(data.__repr__())

    # 返回值
    await chupai.finish(Message(f'{getNameById(id_)}对{getNameById(atSb)}造成了{getCardEffect(cardname)}点伤害！'))
        
backpack = on_keyword(['卡包'], priority=48)
@backpack.handle()
async def backpack_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "卡包":
        await backpack.finish()

    id_ = event.get_user_id()
    data2 = open("C:/bot_things/cardbackpack/" + id_, "a+")
    data2.seek(0)
    data = eval(data2.read())

    if len(data):
        data.sort()
        mess = ""
        for _ in data:
            mess += "["
            mess += str(data.index(_)+1)
            mess += "]"
            mess += getCardValue(_)
            mess += "("
            mess += str(getCardEffect(_))
            mess += ")"
            mess += _
            mess += "\n"
        mess = mess[:len(mess)-1]

        # 用pygame生成图片
        font = pygame.font.Font(os.path.join("C:/Windows/Fonts", "msyh.ttf"), 18)
        rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
        pygame.image.save(rtext, "C:\output.png")

        await backpack.finish(Message(f'{getNameById(id_)}的卡包中有：[CQ:image,file="C:\output.png"]\n收集度：({len(mess)}/400)。'))
    else:
        await backpack.finish(Message(f'{getNameById(id_)}的卡包空空如也。'))
    
helpp = on_keyword(['help'], priority=46)
@helpp.handle()
async def helpp_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "help":
        await helpp.finish()

    mess = "【hrxbot help】\n1.[ycgpa] 预测下一门gpa\n2.[率：xxx] 测试今天xxx率\n3.[选：xxx zzz ...] 随机选一个\n4.已删除\n5.[sudo 选：...] 选100次\n6.[起名：ggg] 给自己起名字\n"
    mess += "7.[battle @sb] 比赛打杜宝\n8.[当前位置] 同一位置的人\n9.[世界] 查看大家都在哪\nA.[移动到：sp] 移动到某地\nB.[smsyyy] 约约约系统帮助\nC.[抽卡/卡包] 卡牌系统"
    await helpp.finish(Message(f'{mess}'))

yyy = on_keyword(['yyy'], priority=46)
@yyy.handle()
async def yyy_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word == "xjyyy":
        data = open("C:/yyy_due.txt").read()
        if int(time.time()) < int(data):
            await yyy.finish(Message(f'当前已经有一个活动的yyy了！还有{(int(data)-int(time.time()))//60}分钟可以创建新的yyy！'))
        data2 = open("C:/yyy_due.txt", "w")
        data2.write(str(int(time.time())+86400))
        data2.close()

        data3 = open("C:/yyy_notes.txt", "w")
        data3.close()

        data3 = open("C:/yyy_participants.txt", "w")
        data3.write(event.get_user_id()+"^")
        data3.close()

        data3 = open("C:/yyy_prayers.txt", "w")
        data3.close()
        await yyy.finish(Message(f'已新建一个yyy，1天后过期。'))

    if word[0:6] == "lyyyy ":
        data7 = open("C:/yyy_due.txt").read()
        if int(time.time()) > int(data7):
            await yyy.finish(Message(f'当前没有活动的yyy!'))

            
        id_ = event.get_user_id()
        data = open("C:/yyy_participants.txt").read()
        if data.count(id_) == 0:
            await yyy.finish(Message(f'你没有参加此yyy，不能留言，只能遥祝。'))
        data2 = open("C:/yyy_notes.txt", "a")
        data2.write("\n"+word[6:])
        data2.close()
        data3 = open("C:/yyy_notes.txt").read()
        await yyy.finish(Message(f'当前yyy的留言是：{data3}'))
        
    if word == "jryyy":
        data6 = open("C:/yyy_due.txt").read()
        if int(time.time()) > int(data6):
            await yyy.finish(Message(f'当前没有活动的yyy!'))
            
        id_ = event.get_user_id()
        data = open("C:/yyy_participants.txt").read()
        if data.count(id_) > 0:
            await yyy.finish(Message(f'你已经参加此yyy，不要重复参加。'))
        data2 = open("C:/yyy_participants.txt", "a")
        data2.write(id_+"^")
        data2.close()
        await yyy.finish(Message(f'你已经参加此yyy。'))

    if word == "yzyyy":
        data7 = open("C:/yyy_due.txt").read()
        if int(time.time()) > int(data7):
            await yyy.finish(Message(f'当前没有活动的yyy!'))
            
        id_ = event.get_user_id()
        data = open("C:/yyy_prayers.txt").read()
        if data.count(id_) > 0:
            await yyy.finish(Message(f'你已经遥祝此yyy，不要重复遥祝。'))
        data2 = open("C:/yyy_prayers.txt", "a")
        data2.write(id_+"^")
        data2.close()
        await yyy.finish(Message(f'你已经遥祝此yyy。'))

    if word == "ckyyy":
        data = open("C:/yyy_due.txt").read()
        if int(time.time()) > int(data):
            await yyy.finish(Message(f'当前没有活动的yyy!'))
        over = (int(data) - int(time.time()))//60
        data2 = open("C:/yyy_notes.txt").read() + "\n"
        nickname_map = open("C:/nickname_map.txt").read()
        data3 = open("C:/yyy_participants.txt").read().split("^")
        data4 = open("C:/yyy_prayers.txt").read().split("^")
        mess = "【当前活动】"
        mess += str(over)
        mess += "分钟后\n【留言】"
        mess += data2
        mess += "【参加人员】"
        for _ in data3:
            if nickname_map.count(_):
                mess += getNameById(_)
            else:
                mess += _
            if _ != data3[len(data3)-1]:
                mess += ", "
            else:
                mess += "\n"
        mess += "【遥祝人员】"
        for _ in data4:
            if nickname_map.count(_):
                mess += getNameById(_)
            else:
                mess += _
            if _ != data4[len(data4)-1]:
                mess += ", "
        await yyy.finish(Message(f'{mess}'))

    if word == "glyyy":
        data = open("C:/yyy_due.txt").read()
        if int(time.time()) > int(data):
            await yyy.finish(Message(f'当前没有活动的yyy!'))
            
        id_ = event.get_user_id()
        data2 = open("C:/yyy_participants.txt")
        data3 = data2.read()
        data4 = data3.split("^")
        data2.close()
        if data3.count(id_):
            data4.remove(id_)
            new_data = ""
            for _ in data4:
                new_data += _
                new_data += "^"
            data5 = open("C:/yyy_participants.txt", "w")
            data5.write(new_data)
            await yyy.finish(Message(f'成功咕掉yyy！'))
        await yyy.finish(Message(f'你没有参加任何yyy！'))

    if word == "ycyyy":
        data2 = open("C:/yyy_due.txt", "w")
        data2.write(str(int(time.time())+86400))
        data2.close()
        await yyy.finish(Message(f'成功延长yyy！1天后结束！'))

    if word == "scyyy":
        data6 = open("C:/yyy_due.txt").read()
        if int(time.time()) > int(data6):
            await yyy.finish(Message(f'当前没有活动的yyy!'))
            
        id_ = event.get_user_id()
        data2 = open("C:/yyy_participants.txt")
        data3 = data2.read()
        data4 = data3.split("^")
        data2.close()
        if data3.count(id_):
            data2 = open("C:/yyy_due.txt", "w")
            data2.write("86400")
            data2.close()
            await yyy.finish(Message(f'成功删除yyy！'))
        await yyy.finish(Message(f'只有yyy发起者才可以删除yyy！'))

    if word == "smsyyy":
        await yyy.finish(Message(f'【yyy帮助】\n新建：xjyyy，新建一个yyy，发起者默认是参与者，默认时长1天。\n留言：lyyyy，参与者给yyy留言。\n加入：jryyy，加入当前yyy。\n遥祝：yzyyy，遥祝当前yyy。\n查看：ckyyy，查看当前活动的yyy内容。\n咕咕：glyyy，取消参加。\n延长：ycyyy，延长yyy的due 1天。\n删除：scyyy，yyy发起者提前结束yyy。'))
    
    
