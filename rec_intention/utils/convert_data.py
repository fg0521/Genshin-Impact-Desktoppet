import copy
import json
import random

import pandas as pd

from utils.connMysql import MySQL
ys_config = {

}
sql = MySQL(config=ys_config)


def deal(x):
    s = eval(x)
    res = [i for i in s if len(i) < 7 and len(i) > 1]
    if len(res) == 1:
        return res[0]
    elif len(res) == 0:
        return ''
    else:
        return res[random.randint(0, len(res) - 1)]

def addSentence(sentence, add, intent, slot):
    n = random.randint(0, len(sentence) - 1)
    m = random.randint(0, len(add) - 1)
    s =sentence[n].replace('*', add[m])
    res = {"text": s, "domain": "yuanshen", "intent": intent, "slots": {slot: add[m]}}
    return s,res

class PrepareData():
    def __init__(self):
        self.role_weapon = ['*的武器是什么','*适合用什么武器','*的专武是什么','有什么武器适合*使用','*配什么武器比较好',
                            '*一般用什么武器']
        self.role_mat = ['*的突破材料有那些','*突破需要什么材料','*升级需要什么东西','*的升级材料都是什么']
        self.role_intro = ['介绍一下*','*是谁','有关*的信息','说一下*吧','关于*','*']
        self.country_intro = ['介绍一下*','*是哪个地方','有关*的信息','说说看*吧','关于*']
        self.all_get = ['*怎么获得','*怎么掉落','我要怎么获取*','*是怎么得来的','要从哪里得到*']
        self.mat_refresh = ['*需要多久时间刷新','隔几天才能得到*','*的刷新时间是多久','*每天都可以获得吗','什么时候可以获得*']
        self.weapon_func = ['*的效果是什么','*有什么作用','*的被动是什么','*能带来什么样的效果','*的作用是什么']


    def get_data(self):
        df = pd.read_csv('../kg_data/characters.csv')
        role_names = df['name'].tolist()
        df1= pd.read_csv('../kg_data/countries.csv')
        country_names = df1['name'].tolist()
        df2 = pd.read_csv('../kg_data/weapons.csv')
        weapon_names = df2['name'].tolist()
        df3 = pd.read_csv('../kg_data/materials.csv')
        material_names = df3['name'].tolist()

        return role_names,country_names,weapon_names,material_names

    def create_data(self,train_cnt=350,test_cnt=70):
        """
                role
                country
                weapon
                material

                roleWeapon
                roleMaterial
                roleIntro
                countryIntro
                materialGet
                materialRefresh
                weaponGet
                weaponFunc

                """
        roles,countries,weapons,materials = self.get_data()
        train = []
        test = []
        sentence = []

        for i in range(train_cnt+test_cnt):

            s1, r1 = addSentence(self.role_weapon, roles, intent='roleWeapon', slot='role')
            s2, r2 = addSentence(self.role_intro, roles, intent='roleIntro', slot='role')
            s3, r3 = addSentence(self.role_mat, roles, intent='roleMaterial', slot='role')

            s4, r4 = addSentence(self.country_intro, countries, intent='countryIntro', slot='country')

            s5, r5 = addSentence(self.weapon_func, weapons, intent='weaponFunc', slot='weapon')
            s6, r6 = addSentence(self.all_get, weapons, intent='weaponGet', slot='weapon')

            s7, r7 = addSentence(self.mat_refresh, materials,intent='materialRefresh',slot='material')
            s8, r8 = addSentence(self.all_get, materials,intent='materialGet',slot='material')


            if i<train_cnt:
                train.extend([r1,r2,r3,r4,r5,r6,r7,r8])
                sentence.extend([s1,s2,s3,s4,s5,s6,s7,s8])
            else:
                test.extend([{'text':r1['text']}, {'text':r2['text']}, {'text':r3['text']}, {'text':r4['text']},
                              {'text':r5['text']}, {'text':r6['text']}, {'text':r7['text']}, {'text':r8['text']}])


        sentence = list(set(sentence))
        train = [str(i) for i  in train]
        train = list(set(train))
        train = [eval(i) for i in train]
        test = [str(i) for i in test]
        test = list(set(test))
        test = [eval(i) for i in test]

        with open('../data/sentences.txt', 'w') as f:
            [f.write(s+'\n') for s in sentence]

        with open('../data/train.json', 'w') as f:
            json.dump(train, f, ensure_ascii=False)

        with open('../data/test.json', 'w') as f:
            json.dump(test, f, ensure_ascii=False)

    def train_test_split(self,ratio=0.8):
        train_file = '../data/train.json'
        with open(train_file, 'r') as fp:
            data = eval(fp.read())
            random.shuffle(data)
            total = len(data)
            train_data = data[:int(total * ratio)]
            test_data = data[int(total * ratio):]
        with open('../data/train_process.json', 'w') as fp:
            json.dump(train_data, fp, ensure_ascii=False)
        with open('../data/test_process.json', 'w') as fp:
            json.dump(test_data, fp, ensure_ascii=False)


if __name__ == '__main__':

    p = PrepareData()
    p.create_data()
    p.train_test_split()
