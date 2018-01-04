# -*- coding: utf-8 -*-
class DefaultParamFactory():
    """
        这个类是内置的，实现了常用的安装参数的实现。
        主要是返回setting中对应到哪个 自定义文件，只有使用自定义命令的时候有用
        现阶段只有Redis Cluster 的实现
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
    def __init__(self,settingInfo,config):
        self.settingInfo=settingInfo
        self.config=config

    def getClusterRedisInstallParam(self):
        return self.settingInfo

