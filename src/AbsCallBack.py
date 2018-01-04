# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbsCallBack():
    """
        回调函数接口，定义了四个回调方法
        分别在
        -- 程序开始前，即配置文件还没有加载到内存中时调用
        -- 配置文件加载到内存中，还没有发给指定的机器运行，即准备启动线程运行
        -- 已经生成了配置文件，和脚本(.sh)文件，你可以修改这些生成的文件，但不要删除和重命名。
        -- 程序执行完成，已经清理完文件。之后
    """
    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def beforeInit(self):
        """ """
        return

    @abstractmethod
    def beforeReadyTiExeSh(self):
        return

    @abstractmethod
    def beforeExeSh(self):
        return

    @abstractmethod
    def afterExeSh(self):
        return
