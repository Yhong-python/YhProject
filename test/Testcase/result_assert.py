#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: result_assert.py
@time: 2020/7/29 17:39
@desc:
'''


import json
from test.Common import global_param
from test.Common.Log import Log
from test.Common.commlib import get_test_data
import jsonpath

log = Log().getlog()







# for key in expected:
#     # 存在以jsonpath规则命名的key时从response中取该jsonpath的字段值来与预期结果进行对比
#     if key.startswith("$") and not key.endswith("$"):
#         respath = jsonpath.jsonpath(response, key)[0]
#         self.log.info("预期校验字段：{}的值为{}；接口返回值的jsonpath：{}的值为{}".format(key, expected[key], key, respath))
#         assert expected[key] == respath
#     else:  # 否则只进行key-value校验
#         self.log.info("预期校验字段：{}的值为{}；接口返回值的key:{}的值为{}".format(key, expected[key], key, response[key]))
#         assert expected[key] == response[key]
apires='{"totalCount":61,"pageSize":10,"totalPage":7,"currentPage":1,"list":[{"id":1,"name":"奇治信息总公司","childNum":8,"statusFlag":1,"contractDate":1924876800000},{"id":134,"name":"发布会试用机构","childNum":4,"statusFlag":1,"contractDate":1633017600000},{"id":187,"name":"测试07","childNum":0,"statusFlag":1,"contractDate":null},{"id":189,"name":"浙江邦融","childNum":0,"statusFlag":1,"contractDate":null},{"id":195,"name":"测试008","childNum":0,"statusFlag":1,"contractDate":null},{"id":197,"name":"合肥一环","childNum":0,"statusFlag":1,"contractDate":null},{"id":199,"name":"河北钮航","childNum":0,"statusFlag":1,"contractDate":null},{"id":200,"name":"合肥天庆大厦","childNum":1,"statusFlag":1,"contractDate":null},{"id":209,"name":"金云汇合肥客服中心","childNum":0,"statusFlag":1,"contractDate":null},{"id":216,"name":"z11","childNum":0,"statusFlag":1,"contractDate":null}]}'
apires=json.loads(apires)
# print(apires)
# print(jsonpath.jsonpath(apires, "$.page.list"))

data = get_test_data('../TestCaseData/organizeManage.yml', 'tests1')
print(type(data[1][1][2]['response']['page']))
print(data[1][1][2]['response']['page'])

