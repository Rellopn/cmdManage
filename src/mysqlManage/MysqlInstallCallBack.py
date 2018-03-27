# -*- coding: utf-8 -*-

from AbsCallBack import AbsCallBack
import os

class MysqlInstallCallBack(AbsCallBack):
    """
        默认的回调类 功能说明建见 AbsCallBacks
    """

    def __init__(self, config):
        """ 初始化的时候传入配置参数"""
        AbsCallBack.__init__(self, config)