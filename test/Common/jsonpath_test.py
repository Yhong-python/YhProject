#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: jsonpath_test.py
@time: 2020/7/23 17:04
@desc:
'''
import jsonpath

result = {'code': 200, 'page': {'totalCount': 61, 'pageSize': 10, 'totalPage': 7, 'currentPage': 1, 'list': [
    {'id': 1, 'name': '奇治信息总公司', 'childNum': 8, 'statusFlag': 1, 'contractDate': 1924876800000},
    {'id': 134, 'name': '发布会试用机构', 'childNum': 4, 'statusFlag': 1, 'contractDate': 1633017600000},
    {'id': 187, 'name': '测试07', 'childNum': 0, 'statusFlag': 1, 'contractDate': None},
    {'id': 189, 'name': '浙江邦融', 'childNum': 0, 'statusFlag': 1, 'contractDate': None},
    {'id': 195, 'name': '测试008', 'childNum': 0, 'statusFlag': 1, 'contractDate': None},
    {'id': 197, 'name': '合肥一环', 'childNum': 0, 'statusFlag': 1, 'contractDate': None},
    {'id': 199, 'name': '河北钮航', 'childNum': 0, 'statusFlag': 1, 'contractDate': None},
    {'id': 200, 'name': '合肥天庆大厦', 'childNum': 1, 'statusFlag': 1, 'contractDate': None},
    {'id': 209, 'name': '金云汇合肥客服中心', 'childNum': 0, 'statusFlag': 1, 'contractDate': None},
    {'id': 216, 'name': 'z11', 'childNum': 0, 'statusFlag': 1, 'contractDate': None}]}}

msg = jsonpath.jsonpath(result, '$.page.list[0].id]')
print(msg)
msg = jsonpath.jsonpath(result, '$.page.list[0].name]')
print(msg)