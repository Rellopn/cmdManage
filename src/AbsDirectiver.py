# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class AbsDirectiver():
    __metaclass__ = ABCMeta
    """
        定义了到底执行哪个方法，把setting中设置的模式和真正执行的类关联起来
        
        :param config 配置文件
    """

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def direction(self):
        """ 组装 """
        return
