#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: commlib.py
@time: 2020/7/22 15:03
@desc:
'''
import jsonpath
from ruamel import yaml
import json
from test.Common import global_param

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


def get_requests_data(data):
    for key, value in data.items():
        print(key, value)
        # if value.startswith("$") and value.endswith("$"):
        #     paramData=global_param.ALL_PARAM['companyList']

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

