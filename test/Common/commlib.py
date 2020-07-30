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
import jsonpath
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
                        if isinstance(value,int):
                            return value
                        else:
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

    def convert(self, casedata):#传入pytest用例读取后的http['data']数据，返回经常处理的可以直接用于接口请求的数据
        if isinstance(casedata, dict):
            for key in casedata:
                casedata[key] = self.convert_value(casedata[key])
            return casedata
        else:
            raise TypeError("传入的数据类型必须为dict,当前传入的数据类型为{}".format(type(casedata)))

def assertResult(expected,apiResult):
    if isinstance(expected,dict):#判断yml中的expected是否为字段格式，不符合时直接抛异常
        expected_response=expected.get('response',None)
        if expected_response:#判断yml中的expected中是否存在response
            if isinstance(expected_response,dict):
                for key in expected_response:
                    if key.startswith("$") and not key.endswith("$"):#key以$开头且不是以$结尾的，将接口返回值进行jsonpath校验
                        jsonpathResult= jsonpath.jsonpath(apiResult,key)
                        if jsonpathResult:#匹配结果非faslse时进行格式校验
                            if len(jsonpathResult) == 1:#只进行单一字段匹配校验
                                try:
                                    assert expected_response[key] == jsonpathResult[0],"单一字段值单项数据预期结果与实际结果不匹配"
                                    log.info("jsonpath：{}单一字段校验成功。预期返回:{},接口返回值jsonpath匹配返回：{}".format(key,expected_response[key],jsonpathResult[0]))
                                except Exception as e:
                                    log.error("jsonpath：{}单一字段校验失败。预期返回:{},接口返回值jsonpath匹配返回：{}".format(key,expected_response[key],jsonpathResult[0]))
                                    log.exception(e)
                                    raise
                            elif len(jsonpathResult)>1 or len(jsonpathResult)==0:#列表格式的多数据校验,如[{}]在列表中存在的所有X字段进行校验
                                try:
                                    assert expected_response[key] == jsonpathResult(apiResult,key),"单一字段值多数据预期结果与实际结果不匹配"
                                    log.info("jsonpath：{}单一字段多数据校验成功。预期返回:{},接口返回值jsonpath匹配返回：{}".format(key,expected_response[key],jsonpathResult))
                                except Exception as e:
                                    log.error("jsonpath：{}单一字段多数据校验失败。预期返回:{},接口返回值jsonpath匹配返回：{}".format(key,expected_response[key],jsonpathResult))
                                    log.exception(e)
                                    raise
                            else:
                                log.error("{}的jsonpath值进行校验时出现未知异常".format(key))
                                raise Exception("{}的jsonpath值进行校验时出现未知异常".format(key))
                        else:
                            log.error("jsonpath匹配失败：{}的匹配数据为{}".format(key,jsonpathResult))
                            raise ValueError("jsonpath匹配失败：{}的匹配数据为{}".format(key,jsonpathResult))
                    else:#否则直接用key-value进行校验
                        if apiResult.get(key,None):
                            try:
                                assert expected_response[key] == apiResult[key]
                                log.info("预期返回值{0}：{1}与接口返回值{0}：{2}匹配成功".format(key,expected_response[key],apiResult[key]))
                            except Exception as e:
                                log.error("预期返回值{0}：{1}与接口返回值{0}：{2}不匹配".format(key,expected_response[key],apiResult[key]))
                                raise
                        else:
                            log.error("返回返回值中不存在该key:{}".format(key))
                            raise KeyError("返回返回值中不存在该key:{}".format(key))
        else:
            raise KeyError("请检查yml文件中该用例的excepted中是否存在response对应的数据")
    else:
        raise ValueError("请检查yml文件中该用例的excepted字段是否符合dict规则")

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
