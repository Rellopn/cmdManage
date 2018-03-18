# -*- coding: utf-8 -*-
from AbsCmdFactory import AbsCmdFactory


class MysqlCmdFactory(AbsCmdFactory):
    """
        生成命令的场，根据参数工厂生成的参数，在此组装成线程执行的命令。

        :param param 从参数工厂生成的settingInfo

        :param setting 配置文件
    """

    def __init__(self, param, setting, bootSetting):
        AbsCmdFactory.__init__(self, param, setting, bootSetting)

    def getMysqlInstallCmd(self):
        # 循环传入的 settingInfo,为每一个配置添加
        for index, oneServe in enumerate(self.param):
            # 命令集合
            cmd = []
            # 首先进入工作目录
            cmd.append({'cd ' + oneServe['workDir']: '0'})