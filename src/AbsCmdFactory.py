# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class AbsCmdFactory():
    __metaclass__ = ABCMeta

    def __init__(self,param, setting, bootSetting):
        self.param = param
        self.setting = setting
        self.bootSetting = bootSetting