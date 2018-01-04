# -*- coding: utf-8 -*-
from src.redisManage.RedisClusterRun import RedisClusterRun
from src.redisManage.RedisClusterCallBack import RedisClusterCallBack

from src.ProInit import ProInit

if __name__ == '__main__':
    # 加载配置信息
    config = ProInit()
    # 初始化回调类
    callback = RedisClusterCallBack(config)
    # 实例化运行类
    run = RedisClusterRun(config)
    # 传入回调类，开始运行
    run.run(callback)