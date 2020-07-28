#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_organizationManage.py.py
@time: 2020/7/27 11:51
@desc:
'''

import warnings

import allure
import jsonpath
import pytest

from test.Common.DB import DB_config
from test.Common.Log import Log
from test.Common.commlib import get_test_data

warnings.simplefilter("ignore", ResourceWarning)


@allure.epic('账号管理')
@allure.feature("组织机构管理")
class TestOrganizationManage:
    log = Log().getlog()
    db = DB_config()
    data = get_test_data('../TestCaseData/organizeManage.yml', "tests1")

    def setup_class(self):
        pass

    @allure.severity("normal")
    @pytest.mark.parametrize("case,http,expected", data[1], ids=data[0])
    @allure.story("XX用例集合")
    @allure.title("{case}")
    def test_getCompanyList(self, env, loginAdmin_session, case, http, expected):
        self.log.info("用例名称：{}".format(case))
        httpmethod = http['method']
        url = env['adminurl'] + http['path']
        headers = http['headers']
        data = http['data']
        expected = expected['response']
        r = loginAdmin_session.sendRequest(url=url, methord=httpmethod, headers=headers, data=data)
        response = r.json()
        self.log.info("接口返回值{}".format(response))
        self.log.info("预期校验值{}".format(expected))
        # print(response)
        # print(expected)
        for key in expected:
            # 存在以jsonpath规则命名的key时从response中取该jsonpath的字段值来与预期结果进行对比
            if key.startswith("$") and not key.endswith("$"):
                respath = jsonpath.jsonpath(response, key)[0]
                self.log.info("预期校验字段：{}的值为{}；接口返回值的jsonpath：{}的值为{}".format(key, expected[key], key, respath))
                assert expected[key] == respath
            else:  # 否则只进行key-value校验
                self.log.info("预期校验字段：{}的值为{}；接口返回值的key:{}的值为{}".format(key, expected[key], key, response[key]))
                assert expected[key] == response[key]
print('111111111111111111111111111111111111')