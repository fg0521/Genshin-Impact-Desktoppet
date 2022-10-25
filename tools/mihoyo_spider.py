import os
import pprint
import re
import time

import pandas as pd
import requests


class RoleSpider():
    def __init__(self):
        self.url ='https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id='
        self.header = {

        }

    def parser(self):
        global false, null, true
        for i in range(6000):
            try:
                url = self.url+str(i)
                false = null = true = ''
                res = requests.get(url)
                # print(res.text)
                res = eval(res.text)
                data = eval(str(res['data']['content']).replace('\\n',''))
                # pprint.pprint(data)
                role_name = data['title']
                info = eval(data['ext'])["c_25"]["filter"]["text"]
                icon = data['icon']
                summary = data['summary']
                html1 = data['contents'][0]['text']
                introduce = re.findall('class="obc-tmp-character__value">(.*?)</div></div>',html1)
                broken = re.findall('class="obc-tmpl__icon-text">([\u4e00-\u9fa5]+)</span></a> <span class="obc-tmpl__icon-num">(\*[\d]+)</span>',html1)
                desc = re.findall('pre-wrap;">(.*?)</p></td>',html1)
                attr = re.findall('pre-wrap; text-align: center;">(.*?)</p>',html1)
                weapons = re.findall('alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">([\u4e00-\u9fa5]+)</span></a> <!----></div></td>',html1)

                html2 = data['contents'][1]['text']
                attack = re.findall('class="obc-tmpl__icon-text">(.*?)</span> ',html2)
                skill_desc = re.findall('obc-tmpl__pre-text">(.*?)</pre>',html2)
                live_desc = re.findall('<td>(.*?)</td></tr><tr><td><div',html2)
                skill_book = re.findall('<span class="obc-tmpl__icon-text">([\u4e00-\u9fa5「」]+)</span></a> <span class="obc-tmpl__icon-num">(\*[\d]+)</span></div></div><div>',html2)

                mz_desc = [i for i in attack if 'span'not in i and 'class' not in i]

                mz_effect = [i for i in live_desc if 'span'not in i and 'class' not in i]

                print(f'{i}:{role_name}')
                df = pd.DataFrame(data=[{'编号':i,'名字':role_name,'介绍':info,'图片':icon,'总结':summary,
                                         '信息':introduce,'突破材料':broken,'武器选择':desc,'圣遗物':attr,'武器':weapons,
                                         'skill_book':skill_book,'命座描述':mz_desc,'技能描述':skill_desc,'命座':mz_effect}])

                if os.path.exists('../rec_intention/kg_data/mihoyo.csv'):
                    df.to_csv('./mihoyo.csv',mode='a',index=False,header=False,encoding='utf-8')
                else:
                    df.to_csv('./mihoyo.csv',index=False,encoding='utf-8')

            except:
                continue
            time.sleep(2)

class MasterSpider():
    def __init__(self):
        self.url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id='

    def parse(self):
        global false, null, true
        false = null = true = ''

        for i in range(5000,8000):
            try:
                url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id=' + str(i)
                res = requests.get(url)
                if res.status_code == 200:
                    html = eval(res.text.replace('\\n',''))
                    # pprint.pprint(html)
                    contents = html['data']['content']['contents'][0]['text']
                    name = html['data']['content']['title']
                    id = html['data']['content']['id']
                    dropping = [i for i in re.findall('<p class="obc-tmpl__material-name">(.*?)</p> ',contents) if len(i)<50]
                    attack = [i for i in re.findall('pre-wrap;">(.*?)</p></td></tr><tr><td ',contents) if len(i)<50]
                    element = [i for i in re.findall('style="">(.*?)</p></td></tr><tr><td ',contents) if len(i)<50]
                    method = [i for i in re.findall('<li><p style="white-space: pre-wrap;">(.*?)</p></li>',contents) if len(i)<50]
                    backstory = [i for i in re.findall('pre-wrap;">(.*?)</p>',contents) if i not in method and i not in attack and '注：'not in i]
                    print(id,name)

                    df = pd.DataFrame(data=[{'id': id, 'name': name, 'dropping': dropping, 'attack': attack, 'element': element,
                                             'method': method, 'backstory': backstory}])

                    if os.path.exists('../rec_intention/kg_data/master2.csv'):
                        df.to_csv('../rec_intention/kg_data/master2.csv', mode='a', index=False, header=False, encoding='utf-8')
                    else:
                        df.to_csv('../rec_intention/kg_data/master2.csv', index=False, encoding='utf-8')
                time.sleep(2)
            except:
                continue


class AreaSpider():
    def __init__(self):
        self.url = 'https://waf-api-takumi.mihoyo.com/common/map_user/ys_obc/v1/map/map_anchor/list?map_id=2&app_sn=ys_obc&lang=zh-cn'

    def parse(self):
        res =requests.get(self.url)
        areas = []
        if res.status_code == 200:
            data_list = eval(res.text)['data']['list']
            for i in data_list:
                for j in i['children']:
                    areas.append({'first_id':i['id'],'first_area':i['name'],'second_id':j['id'],'second_area':j['name']})
                # areas.append({'id':i['id'],'area':i['name'],'second_area':[{'id':j['id'],'area':j['name']} for j in i['children']]})
        df =pd.DataFrame(data=areas)
        df['id'] = [i for i in range(1,len(df)+1)]
        df.to_csv('../rec_intention/kg_data/area_details.csv',index=False)
        pprint.pprint(areas)


class RoleWeaponSpider():
    def __init__(self):
        self.url = 'https://waf-api-takumi.mihoyo.com/common/map_user/ys_obc/v1/map/game_item?map_id=2&app_sn=ys_obc&lang=zh-cn'

    def parse(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            data = eval(res.text)
            roles = data['data']['avatar']['list']
            weapons = data['data']['weapon']['list']
            role_data,weapon_data = [],[]
            for role in roles:
                role_data.append({'name':role['name'],'level':role['level'],'icon_':role['icon']})
            for weapon in weapons:
                weapon_data.append({'name': weapon['name'], 'level': weapon['level'], 'icon': weapon['icon']})
        df1 = pd.DataFrame(data=role_data)
        df2 = pd.DataFrame(data=weapon_data)
        df1['id'] = [i for i in range(1,len(df1)+1)]
        df2['id'] = [i for i in range(1,len(df2)+1)]
        df1.to_csv('../rec_intention/kg_data/all_role.csv', index=False)
        df2.to_csv('../rec_intention/kg_data/all_weapon.csv', index=False)

class AllBiology():
    def __init__(self):
        self.url = 'https://waf-api-takumi.mihoyo.com/common/map_user/ys_obc/v1/map/point/list?map_id=2&app_sn=ys_obc&lang=zh-cn'

    def parse(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            data = eval(res.text)
            labels = data['data']['label_list']
            data_label = []
            for l in labels:
                data_label.append({'id':l['id'],'name':l['name'],'icon':l['icon'],'all_area':l['is_all_area']})

class FoodSpider():
    def __init__(self):
        self.url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id=103'

    def parse(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            data = eval(res.text)['data']['content']['contents'][0]['text']
            pprint.pprint(data)



def clear_role_info():
    df = pd.read_csv('../rec_intention/kg_data/mihoyo.csv')

    df['介绍'] = df['介绍'].apply(lambda x:[i.split('/')[1] for i in sorted(eval(x))])
    df['信息'] = df['信息'].apply(lambda x:eval(x)[:6])
    df['突破材料汇总'] = df['突破材料'].apply(lambda x:[i[0]+i[1] for i in eval(x)[:9]])
    def weapon_desc(x,y):
        x,y = eval(x),eval(y)
        weapons = ['无锋剑', '薙草之稻光', '贯虹之槊', '天空之脊', '和璞鸢', '护摩之杖', '西风长枪', '宗室猎枪', '龙脊长枪', '决斗之枪', '流月针', '喜多院十文字',
                   '黑岩刺枪', '试作星镰', '千岩长枪', '渔获', '匣里灭辰', '黑缨枪', '白缨枪', '钺矛', '铁尖枪', '新手长枪', '四风原典', '不灭月华', '尘世之锁',
                   '天空之卷', '暗巷的酒与诗', '嘟嘟可故事集', '万国诸海图谱', '昭心', '白辰之环', '黑岩绯玉', '祭礼残章', '试作金珀', '忍冬之果', '西风秘典',
                   '匣里日月', '流浪乐章', '宗室秘法录', '异世界行记', '讨龙英杰谭', '魔导绪论', '甲级宝珏', '翡玉法球', '口袋魔导书', '学徒笔记', '终末嗟叹之诗',
                   '阿莫斯之弓', '天空之翼', '冬极白星', '飞雷之弦振', '宗室长弓', '试作澹月', '黑岩战弓', '弓藏', '西风猎弓', '钢轮弓', '幽夜华尔兹', '风花之颂',
                   '绝弦', '苍翠猎弓', '掠食者', '祭礼弓', '暗巷猎手', '破魔之弓', '弹弓', '信使', '鸦羽弓', '神射手之誓', '历练的猎弓', '狼的末路', '松籁响起之时',
                   '天空之傲', '黑岩斩刀', '反曲弓', '猎弓', '无工之剑', '祭礼大剑', '宗室大剑', '雨裁', '白影剑', '衔珠海皇', '恶王丸', '千岩古剑', '钟剑', '桂木斩长正',
                   '西风大剑', '试作古华', '雪葬的星银', '螭骨剑', '以理服人', '飞天大御剑', '沐浴龙血的剑', '铁影阔剑', '白铁大剑', '佣兵重剑', '训练大剑', '磐岩结绿',
                   '斫峰之刃', '雾切之回光', '天空之刃', '风鹰剑', '苍古自由之誓', '暗巷闪光', '腐殖之剑', '试作斩岩', '黑剑', '黑岩长剑', '西风剑', '降临之剑', '匣里龙吟',
                   '祭礼剑', '天目影打刀', '飞天御剑', '冷刃', '笛剑', '暗铁剑', '铁蜂刺', '宗室长剑', '黎明神剑', '吃虎鱼刀', '旅行剑', '银剑','赤沙之杖','圣显之钥','波乱月白经津',
                   '神乐之真意','息灾','赤角石溃杵','猎人之径','森林王器','若水','辰砂之纺锤']
        res = {}
        for i in range(len(y)):
            if y[i] in weapons:
                res[y[i]] = x[i]
            else:
                break
        return res
    df['武器选择'] = df.apply(lambda x: weapon_desc(x['武器选择'], x['武器']), axis=1)
    df['命之座'] = df['命座描述'].apply(lambda x: [eval(x)[::-1][i] for i in range(1,12,2) if 30>len(eval(x))>20][::-1])
    def add_skill_book(x):
        x = eval(x)
        res = {}
        for i in x:
            if i[0] in res:
                res[i[0]]+= int(i[1].replace('*',''))
            else:
                res[i[0]] = int(i[1].replace('*',''))
        return [k+"*"+str(v) for k,v in res.items()]

    df['技能升级汇总'] = df['技能书'].apply(lambda x:add_skill_book(x))
    # print(df['技能升级汇总'])
    df = df[['编号','名字','介绍','信息','突破材料汇总','技能升级汇总','武器选择','命之座']]
    df.to_csv('../rec_intention/kg_data/mihoyo_clear.csv',index=False,encoding='utf-8')


def clear_role_info2():
    df = pd.read_csv('../rec_intention/kg_data/mihoyo_clear.csv')
    df['介绍']=df['介绍'].apply(lambda x:'|'.join(eval(x)))
    df['信息']=df['信息'].apply(lambda x:'|'.join(eval(x)))
    # 数据拆分、拼接  "['火', '蒙德', '四星', '弓']","['8月10日', '西风骑士团', '火', '弓', '小兔座', '飞行冠军']"
    # new_names = ['编号','名字','介绍','信息','突破材料汇总','天赋升级汇总','武器选择','命之座','元素','国家','级别','武器类型']  # 为新生成的列取名
    # df1 = df['介绍'].str.split('|', expand=True)  # 将数据按‘|’拆分
    # df2 = df['信息'].str.split('|', expand=True)  # 将数据按‘|’拆分
    # df.columns = new_names  # 重命名新生成的列名
    # df = df.join(df1)  # 数据合并
    # df.columns = ['编号','名字','介绍','信息','突破材料汇总','天赋升级汇总','武器选择','命之座','元素','国家','级别','武器类型','填装日期','组织','属性2','武器类型2','星座','称号']
    # df = df.join(df2)  # 数据合并
    df.to_csv('../rec_intention/kg_data/mihoyo_clear_cp.csv',index=False,encoding='utf-8')

def add_info():
    df1 = pd.read_csv('../rec_intention/kg_data/mihoyo_clear_cp.csv')
    df2 = pd.read_csv('../rec_intention/kg_data/characters.csv')
    df1.sort_values(by='name', ascending=True, inplace=True)
    df2.sort_values(by='name', ascending=True, inplace=True)
    # print(type(df1),type(df2))
    # print(df1[['name','武器类型']])
    print(df2)
    df1 = df1[['武器类型','组织','突破材料汇总','天赋升级汇总','武器选择','命之座']]
    print(df1)
    # df1.to_csv('../rec_intention/kg_data/df1.csv',index=False,encoding='utf-8')
    # df2.to_csv('../rec_intention/kg_data/df2.csv',index=False,encoding='utf-8')

    df3 = pd.concat([df2,df1],axis=1)
    print(df3)
    df3.columns = list(df2.columns) + ['weapon_type','organization','break_material','skill_material','weapon_choice','lives']
    print(df3[['name','weapon_type']])
    df3.sort_values(by='country', ascending=True, inplace=True)
    df3['id'] = [i for i in range(1,len(df3)+1)]
    # df3.to_csv('../rec_intention/kg_data/characters_cp.csv',index=False,encoding='utf-8')
    # df2['weapon_type'] = ''
    # df2['weapon_choice'] = ''
    # df2['organization'] = ''
    # df2['break_material'] = ''
    # df2['skill_material'] = ''
    # df2['lives'] = ''
    #
    # for _,row in df2.iterrows():
    #     row['weapon_type'] =


def clear_food():
    df = pd.read_csv('../rec_intention/kg_data/food.csv')
    df['info'] = df['info'].apply(lambda x:'|'.join([i.split('/')[1] for i in sorted(eval(x))]))
    df1 = df['info'].str.split('|', expand=True)
    df.drop(['info'], inplace=True, axis=1)
    df1.columns = ['func_type','rarity','getting1']
    # print(df1)
    df = df.join(df1)
    def fill_food_name(name,cond):
        name,cond = str(name),str(cond)
        # print(cond)
        if name != 'nan':
            s = name
        else:
            if cond.startswith('完成烹饪'):
                s = '奇怪的'+cond[4:]
            elif cond.startswith('成功烹饪'):
                s = cond[4:]
            elif cond.startswith('完美烹饪'):
                s = '美味的'+cond[4:]
            else:
                s = 'None'
        return s

    df['name'] = df.apply(lambda x:fill_food_name(x['name'],x['condition']),axis=1)
    df['getting'] = df.apply(lambda x:'【'+str(x['getting1'])+'】'+str(x['getting']),axis=1)
    df.drop(['getting1'],axis=1,inplace=True)
    df.insert(0,'id',[i for i in range(1,len(df)+1)])
    df.to_csv('../rec_intention/kg_data/done/label-food.csv',index=False,encoding='utf-8')
    print(df)

def clear_master():
    df = pd.read_csv('../rec_intention/kg_data/master.csv')
    def get_ele(attack):
        attack = eval(attack)
        e,a = '无',[]
        if attack:
            if attack[0] in ['无','风','火','水','岩','雷','冰','物理','草']:
                e = attack[0]
            attack.remove(attack[0])
            a = attack
        return e

    df['element'] = df.apply(lambda x:get_ele(x['attack']),axis=1)
    df['attack'] = df['attack'].apply(lambda x:str([i for i in eval(x) if i not in ['无','风','火','水','岩','雷','冰','物理','草']]))

    df.to_csv('../rec_intention/kg_data/done/label-master.csv',index=False,encoding='utf-8')
    print(df[['element','attack']])

if __name__ == "__main__":

    clear_master()
    # clear_food()
    # df = pd.read_csv('../rec_intention/kg_data/master.csv')
    # df = df[df['dropping'].str.contains('摩拉')]
    # df.to_csv('../rec_intention/kg_data/master.csv',index=False)
    # print(df)