#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: commlib.py
@time: 2020/7/22 15:03
@desc:
'''
import json

import requests
from ruamel import yaml

from test.Common import global_param
from test.Common.Log import Log

log = Log().getlog()

def get_test_data(test_data_path, test_node):
    case = []  # 存储测试用例名称
    http = []  # 存储请求对象
    expected = []  # 存储预期结果
    setup=[]
    teardown=[]
    with open(test_data_path) as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        test = dat[test_node]
        # if test[0]['setup']!=None:setup.append(test[0]['setup'])
        # if test[0]['teardown']!=None:setup.append(test[0]['teardown'])

        # print(setup,teardown)
        for td in test:
            case.append(td.get('case', ''))
            http.append(td.get('http', {}))
            expected.append(td.get('expected', {}))
    parameters = list(zip(case,http, expected))
    return case, parameters


class GetReqData:
    def convert_value(self, value):
        """
        :param value: 值
        :return: 返回一个转化类型后的值
        """
        if isinstance(value, int):  # int类型的直接返回
            return value
        elif isinstance(value, str):
            # 选判断需要转化的数据中是否存在$x$的引用，存在的话先替换数据
            if value.startswith("$") and value.endswith("$"):
                global_key = value.split("$")[1]  # 取删除标识符号后的数据
                if global_key:  # 不为空时
                    global_value = global_param.ALL_PARAM.get(global_key, None)
                    if global_value:  # 在保存的全局变量中，该变量不为空时替换数据
                        log.info("进行全局变量替换，{}替换为{}".format(value, global_value))
                        value = global_value
                        return json.dumps(value)
                    else:
                        log.error("在global_param.ALL_PARAM保存的全局变量中未找到该key:{}对应的非空数值".format(global_key))
                        raise ValueError("在global_param.ALL_PARAM保存的全局变量中未找到该key:{}对应的非空数值".format(global_key))
                else:
                    log.error("引用全局变量失败，请检查：{}的格式是否符合要求。正确格式例子：$KEY_NAME$".format(value))
                    raise KeyError("引用全局变量失败，请检查：{}的格式是否符合要求。正确格式例子：$KEY_NAME$".format(value))
            else:  # 不需要进行全局变量替换的
                return value
        elif isinstance(value, (list, tuple)):  # list/tuple类型的数据转化成str
            return json.dumps(value)
        elif isinstance(value, dict):  # dict类型的数据转化成str
            return json.dumps(value)
        else:
            return value

    def convert(self, casedata):
        if isinstance(casedata, dict):
            for key in casedata:
                casedata[key] = self.convert_value(casedata[key])
            return casedata
        else:
            raise TypeError("传入的数据类型必须为dict,当前传入的数据类型为{}".format(type(casedata)))


if __name__ == "__main__":
    data = get_test_data('../TestCaseData/organizeManage.yml', 'test2')
    print(data)
    #读取sql字段
    # for i in data[1]:
    #     # print(i[2])
    #     jsonpathresult=jsonpath.jsonpath(i[2], "$.verifty.sql")
    #     if jsonpathresult:
    #         print(jsonpathresult)

    #     if i[2].get("verifty",None):
    #         if  i[2].get("verifty").get("sql"):
    #             print(i[2].get("verifty").get("sql").split(';'))



    # jsonpath.jsonpath(response, key)[0])
        # if j['response'].get("verifty",None):
            #     print(j['response'].get("verifty",None))

    # print(data[1])

    global_param.ALL_PARAM['COMPLIST'] = {"data": {"asa": 1}}

    data = get_test_data('../TestCaseData/organizeManage.yml', "tests1")
    a = GetReqData()
    for casedata in data[1]:
        reqData = a.convert(casedata[1]['data'])
        print(reqData)
        r = requests.post("https://www.baidu.com", data=reqData, verify=False)
