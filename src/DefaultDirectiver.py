# -*- coding: utf-8 -*-
from AbsDirectiver import AbsDirectiver
from redisManage import RedisClusterCallBack
from redisManage import RedisClusterRun


class DefaultDirectiver(AbsDirectiver):
    """
        AbsDirectiver 的默认实现累 参数详细见 AbsDirectiver
    """

    def __init__(self, config):
        AbsDirectiver.__init__(self, config)

    def direction(self):
        """ 重写的 详细见 AbsDirectiver-direction"""
        # 获取配置的模式名称
        pattern = self.config.loadDic
        pattern = pattern['settingYaml']
        pattern = pattern['pattern']

        # 初始化 回调类 typeof ABSCallBack
        callback = None
        # 初始化 运行类 typeof AbsRun
        run = None

        # 具体调用
        if pattern == 'RedisCluster':
            # 实例化 RedisCluster回调类
            callback = RedisClusterCallBack.RedisClusterCallBack(self.config)
            # 实例化 RedisCluster运行类
            run = RedisClusterRun.RedisClusterRun(self.config)
            pass

        # 有相同的父类，无需关心。直接传入回调类，开始运行
        run.run(callback)
