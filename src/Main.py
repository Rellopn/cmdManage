# -*- coding: utf-8 -*-
import DefaultDirectiver
import ProInit

if __name__ == '__main__':
    # 加载配置信息
    config = ProInit.ProInit()
    # 匹配模式 运行
    DefaultDirectiver.DefaultDirectiver(config).direction()