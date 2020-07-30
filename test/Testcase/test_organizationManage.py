#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_organizationManage.py.py
@time: 2020/7/30 10:49
@desc:
'''

import warnings

import allure
import pytest
from test.Common import global_param
from test.Common.DB import DB_config
from test.Common.Log import Log
from test.Common.commlib import get_test_data,GetReqData,assertResult

warnings.simplefilter("ignore", ResourceWarning)


@allure.epic('账号管理')
@allure.feature("组织机构管理")
class TestOrganizationManage:
    log = Log().getlog()
    db = DB_config()
    data = get_test_data('../TestCaseData/organizeManage.yml', "tests1")

    def setup_class(self):
        global_param.ALL_PARAM['CURRENTPAGE']=1

    @allure.severity("normal")
    @pytest.mark.parametrize("case,http,expected", data[1], ids=data[0])
    @allure.story("XX用例集合")
    @allure.title("{case}")
    def test_getCompanyList(self, env, loginAdmin_session, case, http, expected):
        self.log.info("用例名称：{}".format(case))
        httpmethod = http['method']
        url = env['adminurl'] + http['path']
        headers = http['headers']
        reqData = GetReqData().convert(http['data'])
        r = loginAdmin_session.sendRequest(url=url, methord=httpmethod, headers=headers, data=reqData)
        response = r.json()
        assertResult(expected,response)

