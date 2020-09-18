#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: Config.py
@time: 2020/5/12 11:19
@desc:
'''

import configparser
import os

from test.Common.Log import Log
from test.Common.utils import Singleclass

log = Log()
log = log.getlog()


@Singleclass
class Config:
    # titles:
    TITLE_ENVIRONMENT = "environment"
    TITLE_TEST = "test"
    TITLE_PRE = "prod"

    # values:
    # [environment]
    VALUE_SWITCH = "switch"

    # values:
    # [test]
    VALUE_ADMINURL = "adminurl"
    VALUE_DBHOST = "dbhost"
    VALUE_DBPORT = "dbport"
    VALUE_DBUSER = "dbuser"
    VALUE_DBPWD = "dbpwd"
    VALUE_DBNAME = "dbname"
    VALUE_ADMINUSER = "adminuser"
    VALUE_ADMINPWD = "adminpwd"
    VALUE_WEBURL = "weburl"
    VALUE_WEBUSER = "webuser"
    VALUE_WEBPWD = "webpwd"

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    config = configparser.RawConfigParser()

    def __init__(self):
        """
        初始化
        """
        # self.config = configparser.RawConfigParser()
        self.log = log
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件config.ini存在！")

        self.config.read(self.conf_path)
        self.environment_switch = self.get_conf(self.TITLE_ENVIRONMENT, self.VALUE_SWITCH)
        if self.environment_switch == str(0):
            self.adminurl = self.get_conf(self.TITLE_TEST, self.VALUE_ADMINURL)
            self.dbhost = self.get_conf(self.TITLE_TEST, self.VALUE_DBHOST)
            self.dbport = self.get_conf(self.TITLE_TEST, self.VALUE_DBPORT)
            self.dbuser = self.get_conf(self.TITLE_TEST, self.VALUE_DBUSER)
            self.dbpwd = self.get_conf(self.TITLE_TEST, self.VALUE_DBPWD)
            self.dbname = self.get_conf(self.TITLE_TEST, self.VALUE_DBNAME)
            self.adminuser = self.get_conf(self.TITLE_TEST, self.VALUE_ADMINUSER)
            self.adminpwd = self.get_conf(self.TITLE_TEST, self.VALUE_ADMINPWD)
            self.weburl = self.get_conf(self.TITLE_TEST, self.VALUE_WEBURL)
            self.webuser = self.get_conf(self.TITLE_TEST, self.VALUE_WEBUSER)
            self.webpwd = self.get_conf(self.TITLE_TEST, self.VALUE_WEBPWD)

        elif self.environment_switch == str(1):
            self.adminurl = self.get_conf(self.TITLE_PRE, self.VALUE_ADMINURL)
            self.dbhost = self.get_conf(self.TITLE_PRE, self.VALUE_DBHOST)
            self.dbport = self.get_conf(self.TITLE_PRE, self.VALUE_DBPORT)
            self.dbuser = self.get_conf(self.TITLE_PRE, self.VALUE_DBUSER)
            self.dbpwd = self.get_conf(self.TITLE_PRE, self.VALUE_DBPWD)
            self.dbname = self.get_conf(self.TITLE_PRE, self.VALUE_DBNAME)
            self.adminuser = self.get_conf(self.TITLE_PRE, self.VALUE_ADMINUSER)
            self.adminpwd = self.get_conf(self.TITLE_PRE, self.VALUE_ADMINPWD)
            self.weburl = self.get_conf(self.TITLE_PRE, self.VALUE_WEBUSER)
            self.webpwd = self.get_conf(self.TITLE_PRE, self.VALUE_WEBPWD)

    def get_conf(self, section, name):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(section, name)

    def set_conf(self, section, name, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(section, name, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, section):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(section)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)


if __name__ == "__main__":
    a = Config()
    print(id(a))
    b = Config()
    print(id(b))
    # print(Config().adminurl)
    # Config().set_conf('test','name','123')
    # Config().add_conf('pre')
