import copy
import os
import pprint
import re
import time
import pandas as pd
import requests
false = null = true = ''


class MiHoYoSpider():

    def __init__(self):
        self.url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id='
        self.path = 'your save path'
        self.id = 'id list for spider'


    def parse(self):
        """
        code for parsing html
        need to rewrite it
        """
        pass

    def clear(self):
        """
        code for clearing csv file
        need to rewrite it
        """
        pass


class CharacterSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.char_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/character-id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-character.csv'

    def parse(self):
        for i in self.char_id:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                res = eval(res.text)
                data = eval(str(res['data']['content']).replace('\\n', ''))
                # pprint.pprint(data)
                role_name = data['title']
                info = eval(data['ext'])["c_25"]["filter"]["text"]
                icon = data['icon']
                summary = data['summary']
                html1 = data['contents'][0]['text']
                introduce = re.findall('class="obc-tmp-character__value">(.*?)</div></div>', html1)
                broken = re.findall(
                    'class="obc-tmpl__icon-text">([\u4e00-\u9fa5]+)</span></a> <span class="obc-tmpl__icon-num">(\*[\d]+)</span>',
                    html1)
                desc = re.findall('pre-wrap;">(.*?)</p></td>', html1)
                attr = re.findall('pre-wrap; text-align: center;">(.*?)</p>', html1)
                weapons = re.findall(
                    'alt="" class="obc-tmpl__icon"><span class="obc-tmpl__icon-text">([\u4e00-\u9fa5]+)</span></a> <!----></div></td>',
                    html1)
                html2 = data['contents'][1]['text']
                attack = re.findall('class="obc-tmpl__icon-text">(.*?)</span> ', html2)
                skill_desc = re.findall('obc-tmpl__pre-text">(.*?)</pre>', html2)
                live_desc = re.findall('<td>(.*?)</td></tr><tr><td><div', html2)
                skill_book = re.findall(
                    '<span class="obc-tmpl__icon-text">([\u4e00-\u9fa5「」]+)</span></a> <span class="obc-tmpl__icon-num">(\*[\d]+)</span></div></div><div>',
                    html2)
                mz_desc = [i for i in attack if 'span' not in i and 'class' not in i]
                mz_effect = [i for i in live_desc if 'span' not in i and 'class' not in i]
                print(f'{i}:{role_name}')
                df = pd.DataFrame(data=[{'编号': i, '名字': role_name, '介绍': info, '图片': icon, '总结': summary,
                                         '信息': introduce, '突破材料': broken, '武器选择': desc, '圣遗物': attr, '武器': weapons,
                                         'skill_book': skill_book, '命座描述': mz_desc, '技能描述': skill_desc, '命座': mz_effect}])

                if os.path.exists(self.path):
                    df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                else:
                    df.to_csv(self.path, index=False, encoding='utf-8')
                time.sleep(2)

    def clear(self):
        pass


class MasterSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.master_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/master-id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-master.csv'


    def parse(self):
        for i in self.master_id:
            url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id=' + str(
                i)
            res = requests.get(url)
            if res.status_code == 200:
                html = eval(res.text.replace('\\n', ''))
                # pprint.pprint(html)
                contents = html['data']['content']['contents'][0]['text']
                name = html['data']['content']['title']
                id = html['data']['content']['id']
                dropping = [i for i in re.findall('<p class="obc-tmpl__material-name">(.*?)</p> ', contents) if
                            len(i) < 50]
                attack = [i for i in re.findall('pre-wrap;">(.*?)</p></td></tr><tr><td ', contents) if len(i) < 50]
                element = [i for i in re.findall('style="">(.*?)</p></td></tr><tr><td ', contents) if len(i) < 50]
                method = [i for i in re.findall('<li><p style="white-space: pre-wrap;">(.*?)</p></li>', contents) if
                          len(i) < 50]
                backstory = [i for i in re.findall('pre-wrap;">(.*?)</p>', contents) if
                             i not in method and i not in attack and '注：' not in i]
                print(id, name)
                df = pd.DataFrame(
                    data=[{'id': id, 'name': name, 'dropping': dropping, 'attack': attack, 'element': element,
                           'method': method, 'backstory': backstory}])
                if os.path.exists('../rec_intention/kg_data/master2.csv'):
                    df.to_csv('../rec_intention/kg_data/master2.csv', mode='a', index=False, header=False,
                              encoding='utf-8')
                else:
                    df.to_csv('../rec_intention/kg_data/master2.csv', index=False, encoding='utf-8')
            time.sleep(2)

    def clear(self):
        df = pd.read_csv('../rec_intention/kg_data/master.csv')

        def get_ele(attack):
            attack = eval(attack)
            e, a = '无', []
            if attack:
                if attack[0] in ['无', '风', '火', '水', '岩', '雷', '冰', '物理', '草']:
                    e = attack[0]
                attack.remove(attack[0])
                a = attack
            return e

        df['element'] = df.apply(lambda x: get_ele(x['attack']), axis=1)
        df['attack'] = df['attack'].apply(
            lambda x: str([i for i in eval(x) if i not in ['无', '风', '火', '水', '岩', '雷', '冰', '物理', '草']]))

        df.to_csv('../rec_intention/kg_data/done/label-master.csv', index=False, encoding='utf-8')
        print(df[['element', 'attack']])


class FoodSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.food_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/food-id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-food.csv'

    def parse(self):
        pass

    def clear(self):
        df = pd.read_csv('../rec_intention/kg_data/food.csv')
        df['info'] = df['info'].apply(lambda x: '|'.join([i.split('/')[1] for i in sorted(eval(x))]))
        df1 = df['info'].str.split('|', expand=True)
        df.drop(['info'], inplace=True, axis=1)
        df1.columns = ['func_type', 'rarity', 'getting1']
        # print(df1)
        df = df.join(df1)

        def fill_food_name(name, cond):
            name, cond = str(name), str(cond)
            # print(cond)
            if name != 'nan':
                s = name
            else:
                if cond.startswith('完成烹饪'):
                    s = '奇怪的' + cond[4:]
                elif cond.startswith('成功烹饪'):
                    s = cond[4:]
                elif cond.startswith('完美烹饪'):
                    s = '美味的' + cond[4:]
                else:
                    s = 'None'
            return s

        df['name'] = df.apply(lambda x: fill_food_name(x['name'], x['condition']), axis=1)
        df['getting'] = df.apply(lambda x: '【' + str(x['getting1']) + '】' + str(x['getting']), axis=1)
        df.drop(['getting1'], axis=1, inplace=True)
        df.insert(0, 'id', [i for i in range(1, len(df) + 1)])
        df.to_csv('../rec_intention/kg_data/done/label-food.csv', index=False, encoding='utf-8')
        print(df)


class WeaponSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.weapon_id = list(pd.read_csv('../rec_intention/kg_data/mhy-id/weapon_id.csv')['mhy_id'])
        self.path = '../rec_intention/kg_data/to_do/label-weapon.csv'

    def parse(self):
        for i in self.weapon_id:
            url = self.url+str(i)
            res = requests.get(url)
            if res.status_code == 200:
                # pprint.pprint(eval(res.text))
                data = eval(res.text)['data']['content']
                name = data['title']
                id = data['id']
                icon = data['icon']
                ext = eval(eval(data['ext'])["c_5"]["filter"]["text"])
                text = data['contents'][0]['text'].replace('\n','')
                desc = [re.sub('<(.*?)>','',str(i)) for i in re.findall('装备描述(.*?)冒险等阶限制',text)]
                limit = re.findall('obc-tmpl__rich-text">冒险等阶限制：(.*?)</td></tr>',text)
                # getting = [re.sub('<(.*?)>','',str(i)) for i in re.findall('obc-tmpl__rich-text">获取途径：(.*?)</p></td></tr>',text)]
                story = [re.sub('<(.*?)>','',str(i)) for i in re.findall('相关故事(.*?)</p></div>',text)]
                material = [re.sub('<(.*?)>','',str(i)) for i in re.findall('<span class="obc-tmpl__icon-text">(.*?)</span>',text)]
                material_num = [re.sub('<(.*?)>','',str(i)) for i in re.findall('<span class="obc-tmpl__icon-num">(.*?)</span>',text)]
                grade = [re.sub('<(.*?)>','',str(i)) for i in re.findall('class="obc-tmpl__switch-btn">(.*?)</li>',text)]
                effect = [re.sub('<(.*?)>','',str(i)) for i in re.findall('<tbody><tr><td colspan="\d">(.*?)</li></ul></td></tr></tbody>',text)]
                print(name)
                data = [{'name':name,'id':id,'ext':ext,'desc':desc,'limit':limit,'story':story,
                         'material':material,"material_num":material_num,'grade':grade,'effect':effect,'icon':icon}]
                df = pd.DataFrame(data=data)
                if os.path.exists(self.path):
                    df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                else:
                    df.to_csv(self.path, index=False, encoding='utf-8')
                time.sleep(2)

    def clear(self):
        # name,id,ext,desc,limit,getting,story,material,"material_num",grade,effect
        df = pd.read_csv(self.path)
        def split_ext(x):
            x = eval(x)
            res ={'武器类型':'None', '武器星级':'None', '属性加成':'None', '获取途径':'None'}
            for i in x:
                s = i.split('/')
                if res[s[0]] != 'None':
                    res[s[0]] = res[s[0]]+f"、{s[1]}"
                else:
                    res[s[0]] = s[1]
            res = [v for _,v in res.items()]
            return '|'.join(res)

        df['ext'] = df['ext'].apply(lambda x:split_ext(x))
        df1 = df['ext'].str.split('|', expand=True)
        df1.columns = ['weapon_type','rarity','attr_add','getting']
        df = df.join(df1)

        def skill(x,mode=0):
            x= eval(x)
            if not x:
                return 'None'
            else:
                if mode == 0:
                    s = ''.join(re.findall('\)(.*?)·', x[0]))
                    return s if s else 'None'
                else:
                    sp = ''.join(re.findall('\)(.*?)·', x[0]))+'·'
                    return x[0].replace(sp,'')


        df['introd'] = df['desc'].apply(lambda x:skill(x,0))
        df['refine'] = df['desc'].apply(lambda x:skill(x,1))

        def add_material_num(name,num):
            name,num = eval(name),eval(num)
            index = name.index('摩拉')
            res = []
            for i in range(index):
                res.append(name[i]+num[i])
            return str(res)

        df['material'] = df.apply(lambda x:add_material_num(x['material'],x['material_num']),axis=1)
        df['grade'] = df['grade'].apply(lambda x:[i.replace(' ','') for i in eval(x) if '角色' not in i])

        def add_breaking(grade,effect):
            grade,effect = grade,eval(effect)
            res = {}
            for i in range(len(grade)):
                g = grade[i]
                e = effect[i]
                res[g]=e
            return str(res)
        df['breaking'] = df.apply(lambda x:add_breaking(x['grade'],x['effect']),axis=1)
        df = df[['name','id','limit','story','material','icon','breaking','introd','refine','weapon_type','rarity','attr_add','getting']]
        df['limit'] = df['limit'].apply(lambda x:eval(x)[0] if eval(x) else '无')
        df['story'] = df['story'].apply(lambda x:''.join(eval(x)))
        df['label'] = 'weapon'
        print(df.head(10))
        df.to_csv('../rec_intention/kg_data/done/label-weapon.csv',index=False,encoding='utf-8')


class NPCSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.npc = list(pd.read_csv('../rec_intention/kg_data/mhy-id/npc_id.csv')['id'])
        self.path = '../rec_intention/kg_data/to_do/label-npc.csv'

    def parse(self):
        for i in self.npc:
            url = self.url+str(i)
            res = requests.get(url)
            if res.status_code ==200:
                data = eval(res.text)['data']['content']
                name = data['title']
                id = data['id']
                icon = data['icon']
                text = data['contents'][0]['text'].replace('\n','')
                sex = [re.sub('<(.*?)>','',str(i)) for i in re.findall('<td class="h3">性别</td> <td>(.*?)</td>',text)]
                sex = sex[0] if sex else ''
                pos = [re.sub('<(.*?)>','',str(i)) for i in re.findall('<td class="h3">位置</td> <td>(.*?)</td>',text)]
                pos = pos[0] if pos else ''
                task = [re.sub('<(.*?)>','',str(i)) for i in re.findall('<td class="h3">相关任务</td> <td>(.*?)</td>',text)]
                task = task[0] if task else ''
                profession = [re.sub('<(.*?)>','',str(i)) for i in re.findall('class="obc-tmpl__rich-text"><p>(.*?)</p></td></tr>',text)]
                profession = profession[0] if profession else ''
                tips = [re.sub('<(.*?)>', '', str(i)) for i in re.findall('<p style="white-space: pre-wrap;">(.*?)</p></td></tr>', text)]
                tips = list(set(tips))
                print(id,name)
                df = pd.DataFrame(data=[{'nhy_id':id,'name':name,'sex':sex,'pos':pos,'task':task,'profession':profession,'tips':tips,'icon':icon}])
                # pprint.pprint(data)
                if os.path.exists(self.path):
                    df.to_csv(self.path, mode='a', index=False, header=False, encoding='utf-8')
                else:
                    df.to_csv(self.path, index=False, encoding='utf-8')
                time.sleep(2)
    def clear(self):
        df = pd.read_csv(self.path)
        df['task'] = df['task'].apply(lambda x:'暂无' if x in ['无','暂无数据','待录入'] else x)
        df['profession'] = df['profession'].apply(lambda x:'暂无' if x in ['无','暂无数据','待录入'] else x)
        df['tips'] = df['tips'].apply(lambda x:str([i for i in eval(x) if not re.findall('\[每(.*?)日\]|食谱：|\[每周\]| \* |\d',i)]))
        df['tips'] = df['tips'].apply(lambda x:''.join(eval(x)))
        df.fillna('暂无', inplace=True, axis=1)
        df.to_csv('../rec_intention/kg_data/done/label-npc.csv', index=False, encoding='utf-8')
        print(df['tips'])


class BreakMaterialSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()

    def clear(self):
        df = pd.read_csv('../rec_intention/kg_data/breaking_material.csv')
        df = df[['material_id', 'name', 'info']]
        def split_info(x, mode):
            x = (eval(x))
            x = [re.sub('[\d]+级\*(\d\d|\d)[；]*', '', i) for i in x]
            getting_idx, desc_idx, using_idx = -1, -1, -1
            for i in range(len(x)):
                # if '获得方式：' in x[i]:
                #     getting_idx = i
                if x[i].startswith('描述：'):
                    desc_idx = i
                if x[i].startswith('用途：'):
                    using_idx = i
            if mode == 1:
                return ''.join(x[:desc_idx])
            if mode == 2:
                return ''.join(x[desc_idx + 1:using_idx])
            if mode == 3:
                return ''.join(x[using_idx + 1:])

        df['getting'] = df['info'].apply(lambda x: split_info(x, 1))
        df['desc'] = df['info'].apply(lambda x: split_info(x, 2))
        df['using'] = df['info'].apply(lambda x: split_info(x, 3))
        df.drop(['info'], axis=1, inplace=True)
        print(df.head(10))
        df.to_csv('../rec_intention/kg_data/breaking_material1.csv', index=False, encoding='utf-8')


class AreaSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.area_id = list(set(list(pd.read_csv('../rec_intention/kg_data/mhy-id/area-id.csv')['mhy_id'])))
        self.path = '../rec_intention/kg_data/to_do/label-area.csv'

    def parse(self):
        # print(self.area_id)
        a = [1413,115,247,120,121]
        for i in a:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                try:
                    data = eval(res.text)['data']['content']
                    # pprint.pprint(data)
                    id = data['id']
                    icon = data['icon']
                    name = data['title']
                    print(id, name,'get')
                    try:
                        text = data['contents'][0]['text']
                    except:
                        text = data['content']

                    desc = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('简述</td> <td>(.*?)</td>',text)]
                    decryption =[re.sub('<(.*?)>','|',str(i)) for i in re.findall('<h2>机关</h2> (.*?)</tbody></table>',text)]
                    evil_task = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('魔神任务</td> <td>(.*?)</td>',text)]
                    legend_task = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('传说任务</td> <td>(.*?)</td>',text)]
                    delegate_task = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('委托任务</td> <td>(.*?)</td>',text)]
                    world_task = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('世界任务</td> <td>(.*?)</td>',text)]
                    common_master = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('普通怪物</td> <td>(.*?)</td>',text)]
                    elite_master = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('精英怪物</td> <td>(.*?)</td>',text)]
                    boss_master = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('BOSS</td> <td>(.*?)</td>',text)]

                    role_material = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('角色养成素材</td> <td>(.*?)</td>',text)]
                    ingredient = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('食材</td> <td>(.*?)</td>',text)]
                    material = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('材料</td> <td>(.*?)</td>',text)]
                    specialty = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('区域特产</td> <td>(.*?)</td>',text)]


                    # pprint.pprint(data)
                    df = pd.DataFrame(
                        data=[{'mhy_id': id, 'name': name, 'desc': str(desc), 'decryption': str(decryption), 'evil_task': str(evil_task),
                               'legend_task': str(legend_task), 'delegate_task':str(delegate_task),'world_task':str(world_task),
                               'common_master':str(common_master),'elite_master':str(elite_master),'boss_master':str(boss_master),
                               'role_material':str(role_material),'ingredient':str(ingredient),'material':str(material),'specialty':str(specialty),
                               'icon': icon}])
                    if os.path.exists(self.path):
                        df.to_csv(self.path, mode='a', index=False, header=False,encoding='utf-8')
                    else:
                        df.to_csv(self.path, index=False, encoding='utf-8')
                except:
                    print(id, name, 'error')
                    continue
            time.sleep(2)
            # break

    def clear(self):
        df = pd.read_csv(self.path)
        # df['sec_area'] = df['desc'].apply(lambda x:)
        for col in list(df.columns)[3:-1]:
            df[col] = df[col].apply(lambda x:[i for i in eval(x)[0].split('|') if i.replace(' ','').replace('非战斗类','').replace('战斗类','')] if eval(x) else '暂无')
        # print(df['delegate_task'])
        # df1 = pd.read_csv('../rec_intention/kg_data/mhy-id/area-id.csv')
        # area_dic = {}
        # for _,row in df1.iterrows():
        #     area_dic[row['first_area']] = {'second_area':row['second_area'],'country':row['country']}
        # df['sec_area'] = ''
        # df['country'] = ''
        # for idx,row in df.iterrows():
        #     df.loc[idx,'sec_area'] = area_dic[row['name']]['second_area']
        #     df.loc[idx,'country'] = area_dic[row['name']]['country']
        df.to_csv('../rec_intention/kg_data/done/label-area.csv',index=False,encoding='utf-8')


class MaterialSpider(MiHoYoSpider):
    def __init__(self):
        super().__init__()
        self.material_id = list(set(list(pd.read_csv('../rec_intention/kg_data/add_material.csv')['mhy_id'])))
        self.path = '../rec_intention/kg_data/to_do/label-material2.csv'

    def parse(self):
        for i in self.material_id:
            url = self.url + str(i)
            res = requests.get(url)
            if res.status_code == 200:
                try:
                    data = eval(res.text)['data']['content']
                    # pprint.pprint(data)

                    id = data['id']
                    icon = data['icon']
                    name = data['title']
                    print(id, name,'get')
                    try:
                        text = data['contents'][0]['text']
                    except:
                        text = data['content']

                    getting = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('获得方式：</label>(.*?)</td>',text)]
                    description =[re.sub('<(.*?)>','|',str(i)) for i in re.findall('描述：(.*?)</p></td>',text)]
                    using = [re.sub('<(.*?)>','|',str(i)) for i in re.findall('用途：(.*?)</p></td>',text)]

                    # pprint.pprint(data)
                    # mhy_id,name,type,getting,description,using,label
                    df = pd.DataFrame(
                        data=[{'mhy_id': id, 'name': name,'type':'cooking', 'description': str(description), 'getting': str(getting), 'using': str(using),
                               'icon': icon,'label':'material'}])
                    if os.path.exists(self.path):
                        df.to_csv(self.path, mode='a', index=False, header=False,encoding='utf-8')
                    else:
                        df.to_csv(self.path, index=False, encoding='utf-8')
                except:
                    # print(id, name, 'error')
                    continue
            time.sleep(2)
            # break



if __name__ == "__main__":
    df = pd.read_csv('../rec_intention/kg_data/done/label-material.csv')
    df.drop(['label'],axis=1,inplace=True)
    df1 = copy.deepcopy(df)
    df1['icon'] = ''
    for idx,row in df.iterrows():
        id = row['mhy_id']
        url = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/content/info?app_sn=ys_obc&content_id='+str(id)
        res = requests.get(url)
        if res.status_code == 200:
            data = eval(res.text)['data']['content']
            id = data['id']
            icon = data['icon']
            df1.loc[idx,'icon'] = icon
            name = data['title']
            print(name)
        time.sleep(2)
    df1['label'] = 'material'
    df1.to_csv('../rec_intention/kg_data/done/label-material-cp.csv',index=False,encoding='utf-8')

