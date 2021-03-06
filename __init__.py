from nonebot import get_driver
import random
import math
import os
from datetime import date
import time
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import MessageSegment
from .config import Config
import pygame
import os
import re
from pathlib import Path
import urllib.parse

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
    if a < 10:
        return ys_list[3]
    elif a < 25:
        return ys_list[2]
    elif a < 40:
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

add_fungi = on_keyword(['起名：'], priority=46)
@add_fungi.handle()
async def add_fungi_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    name = word[word.find('起名：')+len('起名：'):]
    if len(name) > 20:
        await add_fungi.finish(Message(f'名字太长了！'))
    path = "C:/bot_things/namemap/"
    path += event.get_user_id()
    with open(path, "w", encoding="utf-8") as data:
        data.write(name)
        await add_fungi.finish(Message(f'你好呀，{name}'))
    await add_fungi.finish()

move = on_keyword(['移动到：'], priority=46)
@move.handle()
async def move_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    name = word[word.find('移动到：')+len('移动到：'):]
    path = "C:/bot_things/location/"
    path += event.get_user_id()
    with open(path, "w", encoding="utf-8") as data:
        data.write(name)
        await move.finish(Message(f'你已经移动到{name}！'))
    await move.finish()


baidu = on_keyword(['百度 '], priority=46)
@baidu.handle()
async def baidu_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    name = word[word.find('百度 ')+len('百度 '):]
    prefix = r"https://www.baidu.com/s?ie=utf-8&wd="
    await baidu.finish(Message(f"你不会百度吗？\n{prefix}{urllib.parse.quote(name)}"))


def getNameById(id_):
    path = "C:/bot_things/namemap/"
    namelist = os.listdir(path)
    if id_ not in namelist:
        return id_
    path += id_
    return open(path, encoding="utf-8").read()

here = on_keyword(['当前'], priority=46)
@here.handle()
async def here_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "当前":
        await here.finish()

    path = "C:/bot_things/location/"
    id_ = event.get_user_id()
    yourpath = path + id_
    effect = 0
    with open(yourpath, encoding="utf-8") as data2:
        data = data2.read()

    dirl = os.listdir("C:/bot_things/cardeffect/")
    if id_ not in dirl:
        with open("C:/bot_things/cardeffect/" + id_, "w+", encoding="utf-8") as file:
            file.write("0")

    with open("C:/bot_things/cardeffect/" + id_, encoding="utf-8") as file:
        effect = file.read()

    mess = getNameById(id_) +"，你的经验为"+effect+"\n"
    mess += f"等级为{int(effect)//100+1}，还有{100-int(effect)%100}升级。\n"
    mess += "你当前在"
    if len(data):
        mess += data
    else:
        mess += "未知"
        
    friends = []
    listmap = os.listdir(path)
    for _ in listmap:
        with open(path+_) as g:
            inner = g.read()
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
        with open(path+_) as g:
            mess += g.read()
        mess += "\n"

    mess = mess[:len(mess)-1]
    await lookmap.finish(Message(f'{mess}'))

card_value_list = ['[N] ', '[R] ', '[SR] ', "[SSR] "]
history_up = ["过生日的杜宝"]
up = "过生日的杜宝"

def getCardEffect(s):
    if s == up:
        return len(s) % 3 + 50
    else:
        return len(s) % 3 + 1 + 10 * card_value_list.index(chouka_return((len(s) * 77777) % 100, card_value_list))

def getCardValue(s):
    if s in history_up:
        return "[SP] "
    else:
        return chouka_return((len(s) * 77777) % 100, ['[N] ', '[R] ', '[SR] ', "[SSR] "])


L_name = ["健康打卡", "第二课堂", "林奕含学姐", "66", "蟹老板", "sjj", "顾炎武", "大姐", "美丽学妹珍珠棉", "陈日天", "杜宝", "酚酞女", "原批", "樱桃", "柳杭羽", "史莱姆", "花如雪", "尧尧", "方火华", "lkz", "王梓媛", "gjj"]
L_prefix = ["吃泡面的", "晦气的", "有问题的", "攀岩的", "喝奶茶的", "拍视频的", "打羽毛球的", "踢足球的", "想发paper的", "想染头发的", "好厉害的", "无敌的", "水群的", "flxg的", "吃夜宵的", "做推送的", "菜的", "在报销的", "谈恋爱的", "直播的", "摸鱼的", "躺平的", "内卷的"]

chouka = on_keyword(['抽卡'], priority=48)
@chouka.handle()
async def chouka_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "抽卡":
        await chouka.finish()

    id_ = event.get_user_id()

    if id_ not in os.listdir("C:/bot_things/carddue/"):
        with open("C:/bot_things/carddue/"+id_, "w+", encoding="utf-8") as g:
            g.write("0")

    with open("C:/bot_things/carddue/"+id_, "w+", encoding="utf-8") as g:
        his_time = g.read()

    cd = 60
    flag = False #是否允许抽卡
    if int(time.time()) - int(his_time) > cd:
        flag = True

    if flag:
        # 更新时间
        with open("C:/bot_things/carddue/"+id_, "w+", encoding="utf-8") as g:
            g.write(str(int(time.time())))

        # 抽一张卡
        if random.randint(0, 8) == 9:
            choice = up
        else:
            if id_ == "1025890895":
                choice = random.choice(L_prefix)+random.choice(L_name)
            else:
                choice = random.choice(L_prefix)+random.choice(L_name)

        back = []
        # 打开背包
        with open("C:/bot_things/cardbackpack/"+id_, "a+", encoding="utf-8") as data:
            data.seek(0)
            data2 = data.read()
            if len(data2):
                back = eval(data2)
            else:
                back = []

            # 更新背包
            if choice in back:
                await chouka.finish(Message(f'{getNameById(id_)}抽到了已有卡牌{getCardValue(choice)}{choice}。'))

            back.append(choice)

        with open("C:/bot_things/cardbackpack/"+id_, "w+", encoding="utf-8") as data:
            data.write(back.__repr__())
            await chouka.finish(Message(f'{getNameById(id_)}抽到了新卡{getCardValue(choice)}{choice}！'))

    else:
        await chouka.finish(Message(f'{(int(his.get(id_)) + cd + 1 - int(time.time()))}s后才可再次抽卡！'))

shilian = on_keyword(['十连'], priority=48)
@shilian.handle()
async def shilian_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "十连":
        await shilian.finish()

    id_ = event.get_user_id()

    if id_ not in os.listdir("C:/bot_things/carddue/"):
        with open("C:/bot_things/carddue/"+id_, "w+", encoding="utf-8") as g:
            g.write("0")

    with open("C:/bot_things/carddue/"+id_, "w+", encoding="utf-8") as g:
        his_time = g.read()

    cd = 600
    flag = False #是否允许抽卡
    if int(time.time()) - int(his_time) > cd:
        flag = True

    if flag:
        # 更新时间
        with open("C:/bot_things/carddue/"+id_, "w+", encoding="utf-8") as g:
            g.write(str(int(time.time())))

        back = []
        mess = f"{getNameById(id_)}十连抽到："
        # 打开背包
        with open("C:/bot_things/cardbackpack/"+id_, "a+", encoding="utf-8") as data:
            data.seek(0)
            data2 = data.read()
            if len(data2):
                try:
                    back = eval(data2)
                except:
                    back = []
            else:
                back = []

            # 抽一张卡
            for _ in range(10):
                if random.randint(0, 8) == 9:
                    choice = up
                else:
                    if id_ == "1025890895":
                        choice = random.choice(L_prefix) + random.choice(L_name)
                    else:
                        choice = random.choice(L_prefix) + random.choice(L_name)

                # 更新背包
                if choice in back:
                    mess += "\n"
                    mess += f"已有卡牌{getCardValue(choice)}{choice}。"
                else:
                    mess += "\n"
                    mess += f"新卡{getCardValue(choice)}{choice}！"
                    back.append(choice)

        with open("C:/bot_things/cardbackpack/"+id_, "w+", encoding="utf-8") as data:
            data.write(back.__repr__())
            await shilian.finish(Message(mess))

    else:
        await shilian.finish(Message(f'{(int(his.get(id_)) + cd + 1 - int(time.time()))}s后才可再次抽卡！'))

chupai = on_keyword(['出牌'], priority=48)
@chupai.handle()
async def chupai_handle(bot: Bot, event: Event):
    id_ = event.get_user_id()
    word = str(event.raw_message)
    matchobj = re.match(r"出牌 (.*) (.*?)", word, re.M|re.I)
    print("--------------------------------------------")
    print(matchobj)
    if matchobj is None: # 回血
        matchobj = re.match("出牌 (.*)", word, re.M | re.I)
        if matchobj is None:
            await chupai.finish()
        else:
            cardNum = matchobj.group(1)
            if cardNum.isdecimal() is False:
                await chupai.finish()
            # 打开背包
            data = open("C:/bot_things/cardbackpack/" + id_, "a+")
            data.seek(0)
            data2 = data.read()
            if len(data2):
                try:
                    back = eval(data2)
                except:
                    back = []
            else:
                back = []

            if len(back) < int(cardNum):
                await chupai.finish(Message(f'你没有第{cardNum}张牌！'))
            # 删除卡片
            cardname = back[int(cardNum) - 1]
            back.remove(back[int(cardNum) - 1])
            data = open("C:/bot_things/cardbackpack/" + id_, "w+")
            data.write(back.__repr__())

            # 记录攻击
            data = open("C:/bot_things/cardeffect").read()
            try:
                data = eval(data)
            except:
                data = {}
            data[id_] = str(int(data.get(id_, "0")) + getCardEffect(cardname))
            data2 = open("C:/bot_things/cardeffect", "w+")
            data2.write(data.__repr__())

            # 返回值
            await chupai.finish(Message(f'{getNameById(id_)}获得了{getCardEffect(cardname)}点经验！'))

    cardNum = matchobj.group(1)
    atSb = matchobj.group(2)
    print(atSb)
    if cardNum.isdecimal() is False or atSb.count("qq=")==0:
        await chupai.finish()

    atSb = atSb[atSb.find("=")+1:atSb:find("]")]
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
    cardname = back[int(cardNum)-1]
    back.remove(back[int(cardNum)-1])
    data = open("C:/bot_things/cardbackpack/" + id_, "w+")
    data.write(back.__repr__())

    # 记录攻击
    data = open("C:/bot_things/cardeffect").read()
    data = eval(data)
    data[atSb] = str(int(data.get(atSb, "0")) - getCardEffect(cardname))
    data2 = open("C:/bot_things/cardeffect", "w+")
    data2.write(data.__repr__())

    # 返回值
    await chupai.finish(Message(f'{getNameById(id_)}对{getNameById(atSb)}造成了{getCardEffect(cardname)}点经验伤害！'))
        
backpack = on_keyword(['卡包'], priority=48)
@backpack.handle()
async def backpack_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "卡包":
        await backpack.finish()

    id_ = event.get_user_id()
    data2 = open("C:/bot_things/cardbackpack/" + id_, "a+")
    data2.seek(0)
    data3 = data2.read()
    if len(data3):
        try:
            data = eval(data3)
        except:
            data = []
    else:
        data = []

    if len(data):
        mess = f""
        for _ in data:
            if data.index(_) > 19:
                mess += "最多显示20张牌呢，可以试着出掉前面的卡牌。\n"
                break
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
        font = pygame.font.Font(os.path.join("C:/Windows/Fonts", "simsun.ttc"), 18)
        rtext = font.render(mess, True, (0, 0, 0), (255, 255, 255))
        pygame.image.save_extended(rtext, Path(os.path.join(os.path.dirname(__file__), "resource")) / ("output.png"))

        msg = MessageSegment.text(f"{getNameById(id_)}的卡包中共有{len(data)}张牌\n{mess}\n")
        #msg = MessageSegment.text(f"{getNameById(id_)}的卡包\n收集度：({len(data)}/400)\n") + MessageSegment.image(Path(os.path.join(os.path.dirname(__file__), "resource")) / ("output.png"))
        
        await backpack.finish(message=msg)
    else:
        await backpack.finish(Message(f'{getNameById(id_)}的卡包空空如也。'))
    
helpp = on_keyword(['help'], priority=46)
@helpp.handle()
async def helpp_handle(bot: Bot, event: Event):
    word = str(event.get_message())
    if word != "help":
        await helpp.finish()

    mess = "【hrxbot help】\n" \
           "1.[ycgpa] 预测下一门gpa\n" \
           "2.[率：xxx] 测试今天xxx率\n" \
           "3.[选：xxx zzz ...] 随机选一个\n" \
           "4.已删除\n" \
           "5.[sudo 选：...] 选100次\n" \
           "6.[起名：ggg] 给自己起名字\n"
    mess += "7.已删除\n" \
            "8.[当前] 查看位置和等级\n" \
            "9.[世界] 查看大家都在哪\n" \
            "A.[移动到：sp] 移动到某地\n" \
            "B.[smsyyy] 约约约系统帮助\n" \
            "C.[抽卡/卡包/十连] 卡牌系统\n" \
            "D.[出牌] 按卡包序号出牌"
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
    
    
