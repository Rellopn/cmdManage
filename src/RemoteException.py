# -*- coding: utf-8 -*-
class RemoteException(Exception):
    """ 自定义到错误类 """
    def __init__(self):
        Exception.__init__(self)

    def stractValException(self,index,cmd,stdOut):
        """ 严格执行命令时，验证输出错误"""
        print('执行验证是出错：错误命令在第 '+index+'行，命令是 '+cmd+'. 实际输出为 '+stdOut)