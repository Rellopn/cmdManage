# -*- coding: utf-8 -*-
from src.AbsRun import AbsRun
from src.redisManage.RedisClusterCmdFactory import RedisClusterCmdFactory
from src.ParamFactory import DefaultParamFactory
from src.redisManage.RedisClusterSSHConnect import RedisClusterSSHConnect
from src.ThreadingFactory import ThreadingFactory


class RedisClusterRun(AbsRun):
    """
        这个类定义了 整个程序各个部件的 组装方式，你可以随时获取整个程序的状态

    """

    def __init__(self, config):
        AbsRun.__init__(self, config)
        # 从setting中读取的配置
        self.settingInfo = []
        self.params = None

    def initPro(self, callback):
        """ 初始化 配置文件"""
        # 之前调用回调函数
        callback.beforeInit()
        # 完成后即设置状态加载配置完成
        self.Config.setState(1)

    def readyToExeSh(self, callback):
        """ 在这里，已经生成了配置文件和要传到服务器执行的脚本，你可以修改这些生成的文件，但请不要删除和重命名。"""
        # 之前调用回调函数
        callback.beforeReadyTiExeSh()
        # 获得setting.yaml 中的内容
        settingYaml = self.Config.loadDic['settingYaml']
        # 获得语句
        dpf = DefaultParamFactory(settingYaml['settingInfo'], '')

        self.settingInfo = dpf.getClusterRedisInstallParam()
        dcf = RedisClusterCmdFactory(self.settingInfo, '', self.Config.loadDic['bootstrapYaml'])

        dcf.getYumRedisClusterCmd()
        self.params = dcf.param
        # 状态改变
        self.Config.setState(2)

    def childThread(self, cmd, upfileName, upPath):
        RedisClusterSSHConnect(cmd, self.Config.generateCustSetting).upRun(upfileName, upPath)

    def execSh(self, callback):
        # 之前调用回调函数
        callback.beforeExeSh()
        cmds = self.params
        threads = []
        for cmd in cmds:
            upfileName = 'redisCluster' + str(cmd['id']) + '.sh'
            upPath = cmd['workDir'] + '/redisCluster' + str(cmd['id']) + '.sh'
            t = ThreadingFactory().getThread(self.childThread, (cmd, upfileName, upPath))
            # threading.Thread(target=self.childThread,args=(cmd, upfileName, upPath))
            threads.append(t)
        for thread in threads:
            thread.start()
            thread.join()
        callback.afterExeSh()

    def run(self, callback):
        """ 定义运行方向"""
        self.initPro(callback)
        self.readyToExeSh(callback)
        self.execSh(callback)
