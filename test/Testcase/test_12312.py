#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test.py
@time: 2020/7/23 14:27
@desc:
'''

import warnings

import allure
import pytest

from test.Common import global_param
from test.Common.DB import DB_config
from test.Common.Log import Log
from test.Common.Login import loginAdmin
from test.Common.commlib import get_test_data
from test.Conf.Config import Config

warnings.simplefilter("ignore", ResourceWarning)

@allure.epic('账号管理')
@allure.feature("组织机构管理")
class TestOrganizationManage2:
    log = Log().getlog()
    db = DB_config()
    data = get_test_data('../TestCaseData/organizeManage.yml', "tests1")
    caseids = data[0]
    casedata = list(data[1])


    data2 = get_test_data('../TestCaseData/organizeManage.yml', "test2")
    case2ids = data2[0]
    case2data = list(data2[1])
    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session

    @pytest.mark.parametrize("casename,http,expected", casedata, ids=caseids)
    @allure.title("查看机构列表接口")
    def test_1(self, casename, http, expected):
        httpmethod = http['method']
        apipath = http['path']
        headers = http['headers']
        data = http['data']
        expected = expected['response']
        r = self.base.sendRequest(apipath, httpmethod, headers=headers, data=data)
        response = r.json()

        if expected.get('part_verify', None):
            assert response['page']['list'][0]['id'] == expected['part_verify']['id']
            assert response['page']['list'][0]['name'] == expected['part_verify']['name']
        # global_param.COMPANY_LISAT=response['page']['list']
        global_param.ALL_PARAM['companyList'] = response['page']['list']

    def test_2(self):
        # if global_param.COMPANY_LIST==None:
        #     pytest.skip("依赖接口的数据获取失败")
        # else:
        #     print(global_param.COMPANY_LIST)

        if global_param.ALL_PARAM.get('companyList', None) == None:
            pytest.skip("依赖接口的数据获取失败")
        else:
            print(global_param.ALL_PARAM.get('companyList'))

    # @pytest.mark.parametrize("casename,http,expected", casedata, ids=caseids)
    def test_3(self):
        # paramData=self.case2data[0][1]['data']['getdata']
        # if paramData.startswith("$") and paramData.endswith("$"):
        #     paramData=global_param.ALL_PARAM['companyList']
        # print(paramData)
        paramData=self.case2data[0][1]['data']['search']
        print(paramData)
        print(type(paramData))

        paramData=self.case2data[0][1]['data']['search2']
        print(paramData)
        print(type(paramData))
