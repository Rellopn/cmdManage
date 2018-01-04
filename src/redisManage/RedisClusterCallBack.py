# -*- coding: utf-8 -*-
from src.AbsCallBack import AbsCallBack
import os


class RedisClusterCallBack(AbsCallBack):
    """
        默认的回调类 功能说明建见 AbsCallBacks
    """

    def __init__(self, config):
        """ 初始化的时候传入配置参数"""
        AbsCallBack.__init__(self, config)

    def beforeInit(self):
        print('回调函数调用:beforeInit()')
        return

    def beforeReadyTiExeSh(self):
        print('回调函数调用:beforeReadyTiExeSh()')
        return

    def beforeExeSh(self):
        print('回调函数调用:beforeExeSh()')
        return

    def afterExeSh(self):
        print('回调函数调用:afterExeSh()')
        print('清除生成的文件')
        for oneServer in self.config.loadDic['settingYaml']['settingInfo']:
            for port in oneServer['redisPort']:
                os.remove(str(port) + '.conf')
            os.remove('redisCluster' + str(oneServer['id']) + '.sh')
        print('清除完成')
        return
