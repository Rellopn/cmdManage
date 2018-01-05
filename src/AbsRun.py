# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbsRun():
    """
        这个类定义了 整个程序各个部件的 组装方式，你可以随时获取整个程序的状态.
        每个方法中都传入了一个callback回调函数，回调函数是 接口AbsCallBack 的实现 。默认的实现类是DefaultCallback.
    """

    __metaclass__ = ABCMeta

    def __init__(self, config):
        # 实例化
        self.Config = config

    @abstractmethod
    def initPro(self, callback):
        """ 初始化状态 为1"""
        return

    @abstractmethod
    def readyToExeSh(self, callback):
        """ 准备执行 状态2"""
        return

    @abstractmethod
    def execSh(self, callback):
        """ 执行完成 状态3"""
        return

    @abstractmethod
    def run(self, callback):
        """ 执行"""
        return