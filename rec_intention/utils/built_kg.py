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
    'api':'http://127.0.0.1:7474/',
    'auth':("neo4j", "slash123456")
}
neo4j = Neo4j(config=neo4j_config)

class YuanShen():
    def __init__(self):
        self.char = pd.read_csv('../kg_data/characters.csv')
        self.country = pd.read_csv('../kg_data/countries.csv')
        self.element = pd.read_csv('../kg_data/element.csv')
        self.material = pd.read_csv('../kg_data/materials.csv')
        self.weapon = pd.read_csv('../kg_data/weapons.csv')

    def prepare_data(self):
        """
        转换知识图谱格式数据
        人物标签——(name,{'名称':'糖醋里脊','介绍':'xxxxxx','步骤':'xxxx','材料':'xxx'})
        国家标签——(name,{'名称':'[浙菜,午餐]'})
        元素标签——(name,{'名称':'xxx'})
        材料标签——(name,{'名称':'xxx'})
        武器标签——(name,{})
        一行数据转换成若干组标签元组列表 [(),(),(),(),(),()]
        :param SQL:
        :param sql_str:
        :return:
        """
        # 0:dish  1:main_material  2:sub_material  3:total_material  4:operation  5:introduction  6:category  7:catalog

        self.char.drop(['id','label'],inplace=True,axis=1)
        self.country.drop(['id','label'],inplace=True,axis=1)
        self.element.drop(['id','label'],inplace=True,axis=1)
        self.material.drop(['id','label'],inplace=True,axis=1)
        self.weapon.drop(['id','label'],inplace=True,axis=1)

        # print(type(self.char.to_dict(orient='records')[0]))

        # char = [neo4j.create_node(label='character', attrs=i) for i in self.char.to_dict(orient='records')]
        # country = [neo4j.create_node(label='country', attrs=i) for i in self.country.to_dict(orient='records')]
        # element = [neo4j.create_node(label='element', attrs=i) for i in self.element.to_dict(orient='records')]
        # material = [neo4j.create_node(label='material', attrs=i) for i in self.material.to_dict(orient='records')]
        # weapon = [neo4j.create_node(label='weapon', attrs=i) for i in self.weapon.to_dict(orient='records')]

        # for i in self.char.to_dict(orient='records'):
        #     # c = {}
        #     if i['country'] != 'None':
        #         for j in self.country.to_dict(orient='records'):
        #             if i['country'] == j['name']:
        #                 c=j
        #                 break
        #         neo4j.create_relationship(label1='character', attrs1=i, relationship='come_from',
        #                                   label2='country', attrs2=c)

        for i in self.char.to_dict(orient='records'):
            # c = {}
            if i['element'] != 'None':
                for j in self.element.to_dict(orient='records'):
                    if i['element'] == j['name']:
                        c=j
                        break
                neo4j.create_relationship(label1='character', attrs1=i, relationship='element_is',
                                          label2='element', attrs2=c)


    def built(self, nodes: list, relations: list):
        """
        创建节点和关系用于构建知识图谱
        :param nodes: 存放节点元组的列表
        :param relations: 存放关系元组的列表
        :return:
        """
        pass
        # for node in nodes:
        #     neo4j.create_node(label=node[0], attrs=node[1])
        # for rel in relations:
        #     neo4j.create_relationship(label1=rel[0], attrs1=rel[1], relationship=rel[2], label2=rel[3], attrs2=rel[4])


if __name__ == '__main__':
    # neo4j.del_node(mode='all')
    kg = YuanShen()
    kg.prepare_data()
