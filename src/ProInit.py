# -*- coding: utf-8 -*-
import platform

print 'running on ' + platform.system()
import yaml


class ProInit():
    """"
        初始化资源文档，默认从resource 目录下去读取.
        具体的属性说明请到resource目录下查看。

        关键词：建造者模式、状态模式

        脚本采用state计数来表示当前程序的状态。根据不同的模式（也就是setting.yaml下定义的 pattern 属性）去调用不同的
        方法，组建一套数据。

        程序执行的状态，因为要支持多台服务器的脚本，计划使用多线程来提高效率。
        所以我觉得 通过状态来控制程序执行的阶段是不错的方法。

        现在定义 3种状态
        # 0 默认，无意义。
        # 1 初始化完成 ----  获得setting，加载setting至内存                                    ---|
                         |                                                                     |
                         |  加载配置文件，获得自定义的配置参数，替换或者添加参数                       |
                         |                                                                       |-----在此处 build出数据来
                         |  TODO：未来支持命令参数化，把要执行的命令提出到resource/commond.yaml下.     |
                         |                                                                      |
                         -                                                                     |
                                                                                           ---|
        # 2 准备链接服务器开始执行
        # 3 执行完成 --- 清理链接，退出程序。

        TODO:1、支持自定义配置文件；2、支持从网络上获取配置文件
        :param bootstrap:     基本不会变动的配置文件。
        :param setting:       定义了服务器信息等。
        :param singleConfig:  单机redis 的配置文件，如果setting中设置的
                              模式是集群的话，程序中将会忽略。
        :param clusterConfig: 集群redis 的配置文件，如果setting中设置的
                              模式是单机的话，程序中将会忽略。
        :param genSingC       生成的配置
    """

    # 返回的格式 ：[
    #            {setting:xxxxYaml}
    #            {port:[7001,7002]}
    #            {slave:1}
    #            {username: root}
    #            {password: asd6614250}
    #            {ip: 192.168.1.157}
    #            {sshPort: 22}
    #            {cmd:[
    #                  {ls:'0'}
    #                  {pwd:'/root'}
    #                   ]}
    #             ]
    def __init__(self, bootstrap='../resource/bootstrap.yaml',
                 setting='../resource/setting.yaml',
                 config='../resource/clusterConfig.text'):
        self.setting = setting
        self.bootstrap = bootstrap
        self.config = config

        # 状态码
        self.processState = 0
        self.loadDic = self.loadYaml()

        self.generateCustSetting = self.setAttrToClusterConfig(self.loadDic['settingYaml']['customSetting'])

    def isInit(self):
        """ 判断初始化完成 """
        if self._processState == 1:
            return True
        return False

    def isConnect(self):
        """ 链接至远程服务器完成 """
        if self._processState == 2:
            return True
        return False

    def isDownload(self):
        """ 远程服务器下载完成 """
        if self._processState == 3:
            return True
        return False

    def isPrePareExe(self):
        """ 准备执行 """
        if self._processState == 4:
            return True
        return False

    def isOver(self):
        """ 执行完成 """
        if self._processState == 5:
            return True
        return False

    def setState(self, state):
        """ 设置状态 """
        self.processState = state

    def loadYaml(self):
        """ 加载配置到内存 """
        loadDic = {}
        bootstrap = open(self.bootstrap, 'r')
        bootstrapYaml = yaml.load(bootstrap)

        setting = open(self.setting, 'r')
        settingYaml = yaml.load(setting)

        loadDic['bootstrapYaml'] = bootstrapYaml
        loadDic['settingYaml'] = settingYaml

        bootstrap.close()
        setting.close()

        return loadDic

    def setAttrToSingleConfig(self, customSingles):
        """ 把单机的redis 自定义设置添加或者替换 """
        singleConfig = open(self.config, 'r')
        # clusterConfig = open(self.clusterConfig, 'r')
        # 单例的redis 配置
        sginput = ''
        # 读取一行
        sline = singleConfig.readline()
        # 如果能读到就一直读
        while sline:
            # 循环自定义读[{},{}]
            for index, sc in enumerate(customSingles):
                # 如果index有的话，说明是替换的，当前sline就等于自定义的，然后把自定义的从循环中移走
                # 如果没有的话，当读取完文件后，直接加到配置文件末尾
                try:
                    sline.index(sc.keys()[0])
                    sline = sc.keys()[0] + ' ' + str(sc[str(sc.keys()[0])]) + '\n'
                    # 移除循环
                    del customSingles[index]
                except:
                    pass
            sginput = sginput + sline
            sline = singleConfig.readline()
        # 循环读完 配置文件，customSingles还剩下读就是要添加的
        for index, sc in enumerate(customSingles):
            sginput += sc.keys()[0] + ' ' + str(sc[str(sc.keys()[0])]) + '\n'
        singleConfig.close()
        return sginput

    def setAttrToClusterConfig(self, customCluster):
        """ 把集群的redis 自定义设置添加或者替换 """
        clusterConfig = open(self.config, 'r')
        # 单例的redis 配置
        ccinput = ''
        # 读取一行
        sline = clusterConfig.readline()
        # 如果能读到就一直读
        while sline:
            # 循环自定义读[{},{}]
            for index, sc in enumerate(customCluster):
                # 如果index有的话，说明是替换的，当前sline就等于自定义的，然后把自定义的从循环中移走
                # 如果没有的话，当读取完文件后，直接加到配置文件末尾
                try:
                    sline.index(sc.keys()[0])
                    sline = sc.keys()[0] + ' ' + str(sc[str(sc.keys()[0])]) + '\n'
                    # 移除循环
                    del customCluster[index]
                except:
                    pass

            ccinput = ccinput + sline
            sline = clusterConfig.readline()
        # 循环读完 配置文件，customSingles还剩下读就是要添加的
        for index, sc in enumerate(customCluster):
            ccinput += sc.keys()[0] + ' ' + str(sc[str(sc.keys()[0])]) + '\n'
        clusterConfig.close()
        return ccinput
