import pprint
import re

import pandas as pd

def country2rel():
    df = pd.read_csv('../kg_data/mhy-id/area-id.csv')
    df.columns=['mhy_id','area','place','country']
    df.drop(['mhy_id'],inplace=True,axis=1)
    df.to_csv('../kg_data/done/rel-country-area-place.csv',index=False,encoding='utf-8')

def char2rel():
    df = pd.read_csv('../kg_data/done/label-character.csv')
    df = df[~df['name'].isin(['旅行者（荧）','旅行者（空）'])]
    df = df[['name','element','country','break_material','instance_material','weapon_choice']]

    # df1 = df[['name','element']]
    # df1['rel'] = 'element_is'
    # df1.to_csv('../kg_data/done/rel-character-element.csv',index=False,encoding='utf-8')
    #
    # df2 = df[['name', 'country']]
    # df2['rel'] = 'from'
    # df2.to_csv('../kg_data/done/rel-character-country.csv',index=False,encoding='utf-8')

    # df3 = df[['name','weapon_choice']]
    # df3['weapon_choice'] = df3['weapon_choice'].apply(lambda x:list(eval(x).keys()))
    # data = []
    # for _,row in df3.iterrows():
    #     weapons = row['weapon_choice']
    #     name = row['name']
    #     for w in weapons:
    #         data.append({'name':name,'rel':'using','weapon':w})
    # df3_cp = pd.DataFrame(data=data)
    # df3_cp.to_csv('../kg_data/done/rel-character-weapon.csv', index=False, encoding='utf-8')

    # break_material,skill_material
    for mat in ['break_material','instance_material']:
        df6 = df[['name',mat]]
        data = []
        for _,row in df6.iterrows():
            name = row['name']
            breaking = eval(row[mat])
            for b in breaking:
                b = re.sub('\*\d+','',b)
                data.append({'name':name,'rel':mat,'material':b})
        pprint.pprint(data)
        df6_cp = pd.DataFrame(data=data)
        df6_cp.to_csv(f'../kg_data/done/rel-character-{mat}.csv',index=False,encoding='utf-8')


def char2food():
    df = pd.read_csv('../kg_data/done/label-food.csv')
    df = df[['name','description']]
    data = []
    for _,row in df.iterrows():
        role = re.findall('(.*?)的特色料理',row['description'])
        name = row['name']
        if role:
            data.append({'name':role[0],'rel':'characteristics_of_food','food':name})
    pprint.pprint(data)
    df_cp = pd.DataFrame(data=data)
    df_cp.to_csv('../kg_data/done/rel-character-food.csv',index=False,encoding='utf-8')

def food2material():
    df = pd.read_csv('../kg_data/done/label-food.csv')
    df = df[['name', 'ingredient']]
    data = []
    for _,row in df.iterrows():
        material = eval(row['ingredient'])
        food = row['name']
        for m in material:
            m = re.sub('\*\d+','',m)
            data.append({'food':food,'rel':'ingredient','material':m})
    df_cp = pd.DataFrame(data=data)
    df_cp.to_csv('../kg_data/done/rel-food-material.csv',index=False,encoding='utf-8')


def master2material():
    df = pd.read_csv('../kg_data/done/label-master.csv')
    df = df[['name','dropping']]
    data=[]
    for _,row in df.iterrows():
        master = row['name']
        for m in eval(row['dropping']):
            data.append({'master':master,'rel':'drop_from','material':m})
    df_cp = pd.DataFrame(data=data)
    df_cp.to_csv('../kg_data/done/rel-master-material.csv',index=False,encoding='utf-8')


def weapon2material():
    df = pd.read_csv('../kg_data/done/label-weapon.csv')
    df = df[['name','material']]
    data = []
    for _,row in df.iterrows():
        weapon = row['name']
        for m in eval(row['material']):
            m= re.sub('\*\d+','',m)
            data.append({'weapon':weapon,'rel':'breaking_material','material':m})
    df_cp = pd.DataFrame(data=data)
    df_cp.to_csv('../kg_data/done/rel-weapon-material.csv',index=False,encoding='utf-8')


def look4material():
    df = pd.read_csv('../kg_data/done/label-character.csv')
    df1 = pd.read_csv('../kg_data/done/label-food.csv')
    df2 = pd.read_csv('../kg_data/done/label-material.csv')
    material = []
    for _,row in df.iterrows():
        m1 = [re.sub('\*[\d]+','',i) for i in eval(row['break_material'])]
        m2 = [re.sub('\*[\d]+','',i) for i in eval(row['skill_material'])]
        material.extend(m1)
        material.extend(m2)
    for _,row in df1.iterrows():
        m3 = [re.sub('\*[\d]+','',i) for i in eval(row['ingredient'])]
        material.extend(m3)

    mat = [i.replace('「','').replace('」','') for i in list(df2['name'])]
    add_material = list(set(material)-set(mat))
    df3 = pd.read_csv('../kg_data/master2.csv')
    df5 = pd.read_csv('../kg_data/materials.csv')
    data = []
    for _,row in df3.iterrows():
        id = row['id']
        name = row['name']
        if name in add_material:
            data.append({'mhy_id':id,'name':name})
            add_material.remove(name)
    for _,row in df5.iterrows():
        name = row['name']
        if name in add_material:
            data.append({'mhy_id':0,'name':name})
            add_material.remove(name)
    for n in add_material:
        data.append({'mhy_id':-1,'name':n})
    df4 = pd.DataFrame(data=data)
    print(add_material)
    df4.to_csv('../kg_data/add_material.csv', index=False, encoding='utf-8')


"""
{'钩钩果', '盐', '须弥蔷薇', '秃秃豆', '龙嗣伪鳍', '面粉', '绝云椒椒', '落落莓', '胡椒', '火腿', '风车菊', '蘑菇', '鳗肉', 
'番茄', '鸟蛋', '琉璃百合', '松茸', '劫波莲', '竹笋', '圣金虫', '海草', '日落果', '熏禽肉', '珊瑚真珠', '牛奶', '虾仁', 
'奶酪', '小灯草', '血斛', '赤念果', '星蕈', '培根', '蟹黄', '慕风蘑菇', '幽灯蕈', '稻米', '绯樱绣球', '祸神之禊泪', 
'月莲', '夜泊石', '卷心菜', '晶化骨髓', '甜甜花', '霓裳花', '苹果', '金鱼草', '凶将之手眼', '胡萝卜', '奶油', '薄荷', 
'蒲公英籽', '冷鲜肉', '枣椰', '鬼兜虫', '塞西莉亚花', '天云草实', '莲蓬', '星螺', '摩拉', '兽境王器', '黄油', '兽肉', 
'松果', '禽肉', '嘟嘟莲', '帕蒂沙兰', '糖', '豆腐', '生长碧翡碎屑', '洋葱', '螃蟹', '香肠', '石珀', '堇瓜', '鱼肉', 
'树王圣体菇', '马尾', '琉璃袋', '鸣草', '清心', '香辛料', '树莓', '海灵芝', '杏仁', '墩墩桃', '果酱', '土豆', '万劫之真意', '白萝卜'}


"""
if __name__ == '__main__':
    weapon2material()
    # look4material()
    # df = pd.read_csv('../kg_data/area_details.csv')
    # df['place'] = df['second_area']
    # df.drop(['first_id','first_area','second_id','second_area','id'],inplace=True,axis=1)
    # df['mhy_id'] = [i for i in range(1,len(df)+1)]
    # df['label']='place'
    # df.to_csv('../kg_data/done/label-place.csv',index=False,encoding='utf-8')