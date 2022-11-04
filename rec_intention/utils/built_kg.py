import pandas

# Slash: KnowledgeGraph 2.0
# 集成类TranslateKG，合并原有的三个类，增加可选项，提高代码利用率
# 新增函数get_obj2att，来生成所需要的关系-主体-属性字典
# 新增 description节点用于存放知识图谱的基本描述信息,随知识图谱的更新而更新

import copy
import time
import pprint
import re
import pandas as pd
from connNeo4j import Neo4j

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
neo4j_config = {
    'api': 'http://127.0.0.1:7474/',
    'auth': ("neo4j", "slash123456")
}
neo4j = Neo4j(config=neo4j_config)


class YuanShen():
    def __init__(self):
        self.character = pd.read_csv('../kg_data/done/label-character.csv')
        self.material = pd.read_csv('../kg_data/done/label-material.csv')
        self.area = pd.read_csv('../kg_data/done/label-area.csv')
        self.element = pd.read_csv('../kg_data/done/label-element.csv')
        self.weapon = pd.read_csv('../kg_data/done/label-weapon.csv')
        self.master = pd.read_csv('../kg_data/done/label-master.csv')
        self.food = pd.read_csv('../kg_data/done/label-food.csv')
        self.npc = pd.read_csv('../kg_data/done/label-npc.csv')
        self.country = pd.read_csv('../kg_data/done/label-country.csv')
        self.place = pd.read_csv('../kg_data/done/label-place.csv')

    def built(self, node=False, relationship=False):
        """
        创建节点和关系用于构建知识图谱
        :param nodes: 存放节点元组的列表
        :param relations: 存放关系元组的列表
        :return:
        """
        if node:
            # for data in ['self.character','self.material','self.area','self.element','self.weapon',
            #              'self.master','self.food','self.npc','self.country','self.place']:
            for data in ['self.material']:
                df = eval(data)
                df.fillna('暂无', inplace=True)
                df['mhy_id'] = df['mhy_id'].apply(lambda x: str(x))
                df.drop(['label'], inplace=True, axis=1)
                df = df.to_dict(orient='records')
                label = data.replace('self.', '')
                unique_key = 'name' if label == 'foot' else 'mhy_id'
                [neo4j.create_node(label=label, attrs=i, unique_key=unique_key) for i in df]
        if relationship:
            # # country-area-place
            # country = self.country.to_dict(orient='records')
            # area = self.area.to_dict(orient='records')
            # place = self.place.to_dict(orient='records')
            # df = pd.read_csv('../kg_data/mhy-id/area-id.csv')
            # for _, row in df.iterrows():
            #     c = row['country']
            #     a = row['first_area']
            #     p = row['second_area']
            #     label_country = [i for i in country if i['name'] == c]
            #     label_area = [i for i in area if i['name'] == a]
            #     label_place = [i for i in place if i['name'] == p]
            #     if label_country and label_area and label_place:
            #         neo4j.create_relationship(label1='place', attrs1=label_place[0], relationship='part_of',
            #                                   label2='area', attrs2=label_area[0], unique_key1='name',
            #                                   unique_key2='name')
            #         neo4j.create_relationship(label1='area', attrs1=label_area[0], relationship='part_of',
            #                                   label2='country', attrs2=label_country[0], unique_key1='name',
            #                                   unique_key2='name')

            # character-country-element-weapon
            character = self.character.to_dict(orient='records')
            country = self.country.to_dict(orient='records')
            element = self.element.to_dict(orient='records')
            weapon = self.weapon.to_dict(orient='records')
            char_country = pd.read_csv('../kg_data/done/rel-character-country.csv')
            char_element = pd.read_csv('../kg_data/done/rel-character-element.csv')
            char_weapon = pd.read_csv('../kg_data/done/rel-character-weapon.csv')
            for _, row in char_country.iterrows():
                c = row['country']
                name = row['name']
                rel = row['rel']
                label_country = [i for i in country if i['name'] == c]
                label_char = [i for i in character if i['name'] == name]
                if label_country and label_char:
                    neo4j.create_relationship(label1='character', attrs1=label_char[0], relationship=rel,
                                              label2='country', attrs2=label_country[0], unique_key1='name',
                                              unique_key2='name')
            for _, row in char_element.iterrows():
                c = row['element']
                name = row['name']
                rel = row['rel']
                label_element = [i for i in element if i['name'] == c]
                label_char = [i for i in character if i['name'] == name]
                if label_element and label_char:
                    neo4j.create_relationship(label1='character', attrs1=label_char[0], relationship=rel,
                                              label2='element', attrs2=label_element[0], unique_key1='name',
                                              unique_key2='name')
            for _, row in char_weapon.iterrows():
                c = row['weapon']
                name = row['name']
                rel = row['rel']
                label_weapon = [i for i in weapon if i['name'] == c]
                label_char = [i for i in character if i['name'] == name]
                if label_weapon and label_char:
                    neo4j.create_relationship(label1='character', attrs1=label_char[0], relationship=rel,
                                              label2='weapon', attrs2=label_weapon[0], unique_key1='name',
                                              unique_key2='name')






if __name__ == '__main__':
    # neo4j.del_node(mode='all')
    kg = YuanShen()
    kg.built(node=True)
