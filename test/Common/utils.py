#!/usr/bin/env python
# encoding: utf-8
'''
@author: yanghong
@file: utils.py
@time: 2020/9/18 14:21
@desc:
'''


# 单例模式装饰器
def Singleclass(cls):
    __instance = {}

    def _Singleclass(*args, **kwargs):
        if cls not in __instance:
            __instance[cls] = cls(*args, **kwargs)
            return __instance[cls]
        else:
            return __instance[cls]

    return _Singleclass
