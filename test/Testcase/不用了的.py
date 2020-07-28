#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: test_organizationManage.py
@time: 2020/5/8 10:18
@desc:账号管理-组织机构管理
'''
import json
import time
import warnings
import jsonpath
import allure
import pytest
from test.Common import global_param
from test.Common.DB import DB_config
from test.Common.Login import loginAdmin
from test.Common.Log import Log
from test.Conf.Config import Config
from test.Common.commlib import get_test_data
warnings.simplefilter("ignore", ResourceWarning)


@allure.epic('账号管理')
@allure.feature("组织机构管理")
class TestOrganizationManage:
    log = Log().getlog()
    db = DB_config()
    # test = Assertions()
    data=get_test_data('../TestCaseData/organizeManage.yml',"tests1")
    print(data)
    print(data[0])
    # caseids=data[0]
    # casedata=data[1]
    # print(casedata)
    def setup_class(self):
        self.base = loginAdmin(usr=Config().adminuser, pwd=Config().adminpwd)  # 用同一个登录成功后的session
        # pass
    @allure.severity("normal")
    @pytest.mark.parametrize("casename,http,expected",data[1],ids=data[0])
    @allure.title("查看机构列表接口")
    def test_getCompanyList(self,casename,http,expected):
        # print(env)
        httpmethod=http['method']
        apipath=http['path']
        headers=http['headers']
        data=http['data']
        # sql=jsonpath.jsonpath(expected.get('verifty'), "$.sql")
        # print(sql)
        # if sql:print(expected.get('verifty').get("sql"))
        expected=expected['response']
        # data['search']=json.dumps(data['search'])
        r=self.base.sendRequest(apipath,httpmethod,headers=headers,data=data)
        response=r.json()
        # print(response)
        print(expected)

        #校验方法一
        # if expected.get('part_verify',None):
        #     assert response['page']['list'][0]['id']==expected['part_verify']['id']
        #     assert response['page']['list'][0]['name']==expected['part_verify']['name']
            # print('111111111111111111')

        #校验方法二，jsonpath
        for key,value in expected.items():
            print(key,value)
            if key.startswith("$") and not key.endswith("$"):
                print(expected[key],jsonpath.jsonpath(response, key)[0])
                assert expected[key] == jsonpath.jsonpath(response, key)[0]
            else:
                assert expected[key] == response[key]
        # assert expected['code'] == response['code']
                # def test4(self):
    #     print(global_param.COMPANY_LIST)



