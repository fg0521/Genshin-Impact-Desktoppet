"""
@author: Slash
@desc: 知识图谱数据库连接，用于对知识图谱数据的增删改查
@time: 2022/10/11
"""
# coding:utf-8
# from tabulate import tabulate
from py2neo import Node, Relationship, Graph, NodeMatcher

class Neo4j():
    """
    用于图谱数据库的增删改查
    """
    def __init__(self, config):
        self.config = config
        self.graph = Graph(self.config['api'], auth=self.config['auth'])

    def search_node(self, label, attrs):
        """
        :param label: 节点标签
        :param attrs: 节点属性键值对
        :return: 匹配到的节点
        """
        name = list(attrs.keys())[0]
        n = f"_.{name}" + "=" + "\"" + attrs[name] + "\""
        matcher = NodeMatcher(self.graph)
        res = matcher.match(label).where(n).first()
        return res if res else ''

    def create_node(self, label, attrs):
        """
        :param label: 节点标签
        :param attrs: 节点属性键值对
        :return: 创建节点
        """
        assert attrs, "The attr can't be None!"
        name = list(attrs.keys())[0]
        if not self.search_node(label, attrs):
            node = Node(label, **attrs)
            self.graph.create(node)
            print(f'「{attrs[name]}」: Succeed to build Node')
        else:
            print(f'「{attrs[name]}」: Node already existed')

    def create_relationship(self, label1, attrs1, relationship, label2, attrs2):
        """
        :param label1: 节点标签1
        :param attrs1: 节点属性键值对1
        :param relationship: 节点1和节点2的关系
        :param label2: 节点标签2
        :param attrs2: 节点属性键值对2
        :return:
        """
        assert attrs1 and attrs2,"The attr can't be None!"
        node1 = self.search_node(label1, attrs1)
        node2 = self.search_node(label2, attrs2)
        if node1 and node2:
            r = Relationship(node1, relationship, node2)
            self.graph.create(r)
            print(f'「{relationship}」: Succeed to built relationship')
        else:
            print(f'「{relationship}」: Failed to built relationship')

    def del_node(self, label=None, attrs=None, mode='one'):
        """
        :param label: 需要删除的节点标签
        :param attrs: 需要删除的节点属性键值对
        :param mode: 删除1个/所有节点
        :return:
        """
        if mode == 'one':
            assert attrs, "The attr can't be None!"
            name = list(attrs.keys())[0]
            node = self.search_node(label, attrs)
            self.graph.delete(node),print(f'「{attrs[name]}」: Node already deleted') if node else print(f'「{attrs[name]}」: Node not existed')
        if mode == 'all':
            self.graph.delete_all()
            print('All nodes already deleted')

    def updata_node(self, label, org_attrs, new_attrs):
        """
        :param label: 需要更新的节点
        :param org_attrs: 节点原有属性值
        :param new_attrs: 节点更新属性值
        :return:
        """
        # org_attrs包含key即可
        assert org_attrs, "The attr can't be None!"
        name = list(org_attrs.keys())[0]
        node = self.search_node(label, org_attrs)
        node.update(new_attrs),self.graph.push(node),print(f'「{org_attrs[name]}」: Node already updated') if node else print(f'「{org_attrs[name]}」: Node not existed')


    def select(self, label=None, rel=None, condition=None,limit=25,reverse=False,att=None):
        """
        :param condition: 设定查询条件 Dict   condition_key:condition_value
        :param label1: 用于查询标签 Str  ==>  公司名称 公司简称 法定代表人 登记机关 统一社会信用代码
        :param rel: 用于查询关系 关系 Str   ==>  简称 法定代表人 登记机关 统一社会信用代码
        :param limit: 返回节点数限制 Int
        :param reverse: True为通过关系和结果推导主体（反向）  False为通过主体和关系查询结果（正向）Bool
        :param att: 返回节点的某些属性 List
        :return: 节点信息、节点属性信息、节点间关系信息
        """
        cql=''
        limit_str = f' limit {limit}' if limit else ''

        # 默认查询全部 match (n) return n limit 25
        if label is None and rel is None and condition is None:
            cql= f'match (n) return n'

        # 查询某个标签节点 match (n:`公司名称`) where n.公司名称='四川川宝科技有限公司' return n
        elif label is not None and rel is None:
            if condition is None:
                cql = f'match (n:{label}) return n'
            else:
                c = ''
                for k, v in condition.items():
                    c += "n." + k + "=" + "'" + v + "'" + ' and '
                cql = f'match (n:{label}) where ' + c[:-5] + ' return n'

        # 查询某种关系 match p=()-[r:法定代表人]->() return  p limit 25
        elif label is None and rel is not None:
            cql = f'match p=()-[r:{rel}]->() return p'

        # 节点1和关系查询节点2 关系和节点2查询节点1
        elif label is not None and rel is not None:
            ret = "m" if reverse else "n"
            ret1 = "n" if reverse else "m"
            # for k, v in condition.items():
            c = [ret+'.' + k + "=" + "'" + v + "'" for k, v in condition.items()]
            c = ' and '.join(c)
                # c += ret+'.' + k + "=" + "'" + v + "'" + ' and '
            cql = f'match (n:{label})-[r:{rel}]-(m) where ' + c + ' return ' + ret1

        if att:
            tail = cql[-1]
            s = [tail + '.' + i for i in att]
            s = ','.join(s)
            cql = cql[:-1] + s
        cql = cql+limit_str
        result = self.graph.run(cql)
        return result.data




