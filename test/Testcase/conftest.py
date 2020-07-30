#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: conftest.py
@time: 2020/7/23 11:56
@desc:
'''
import os

import pytest
from ruamel import yaml

from test.Common.DB import DB_config
from test.Common.Log import Log
from test.Common.base import Base

log = Log().getlog()


def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     dest="environment",
                     default="test",
                     help="environment: test or prod")


# 配置文件读取的前置操作
@pytest.fixture(scope='session')
def env(request):
    # request.config.rootdir属性，这个属性表示的是pytest.ini这个配置文件所在的目录
    config_path = os.path.join(request.config.rootdir,
                               "Conf",
                               # "test",
                               request.config.getoption("environment"),  # 取变量
                               "config.yml")
    try:
        with open(config_path) as f:
            env_config = yaml.load(stream=f.read(), Loader=yaml.SafeLoader)
    except FileNotFoundError as e:
        log.error("配置文件路径异常，请检查文件路径")
        log.exception(e)
        raise
    except Exception as e:
        log.error("未知异常")
        log.exception(e)
        raise
    else:
        return env_config


# 登录的前置操作
@pytest.fixture(scope='session')
def loginAdmin_session(env, request):
    """
    使用其他账号登录时需要在方法前加上修饰符
    @pytest.mark.parametrize("loginAdmin_session",[{"user":"19999999999","pwd":"999999"}],indirect=True) #使用别的账号登录
    用例中可以申明后会再次请求一次该前置操作，请求会会使用新的账号。下一个用例再次请求时会恢复成默认账号
    :param env:
    :param request: [{}]这种形式
    :return: 登录后的session

    """
    base = Base()
    url = env['adminurl'] + '/adminApi/admin/sys/login'
    usr = env['admin_userInfo']['adminuser']
    pwd = env['admin_userInfo']['adminpwd']
    try:
        usr = request.param['user']
        pwd = request.param['pwd']
    except AttributeError as e:
        log.info('本次测试未指定后台账号,默认登录账号为%s' % usr)
    except Exception as e:
        log.error("指定后台登录账号密码出现未知异常")
        log.exception(e)
    login_data = {'username': usr,
                  'password': pwd,
                  'captcha': '1111'}
    print("本次登录账号信息为%s,%s" % (usr, pwd))
    try:
        r = base.sendRequest(url=url, methord='post', data=login_data)
        print("登录接口返回值:", r.json())
        log.info("登录接口返回值:", r.json())
        assert r.json()['code'] == 200, '后台登录失败，本次测试无效'
    except Exception:
        raise
    return base


# 数据库连接的前置操作
@pytest.fixture(scope='session')
def db_connect(env):
    try:
        host = env['db_info']['dbhost']
        port = env['db_info']['dbport']
        user = env['db_info']['dbuser']
        pwd = env['db_info']['dbpwd']
        dbname = env['db_info']['dbname']
    except KeyError as e:
        log.error("获取配置文件中的数据库信息有误,请检查配置文件")
        log.exception(e)
    except Exception as e:
        log.exception(e)
        raise
    else:
        db = DB_config(host=host, port=port, user=user, passwd=pwd, db=dbname)
        yield db
        db.close()
