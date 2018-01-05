# -*- coding: utf-8 -*-
from src.DefaultDirectiver import DefaultDirectiver
from src.ProInit import ProInit

if __name__ == '__main__':
    # 加载配置信息
    config = ProInit()
    # 匹配模式 运行
    DefaultDirectiver(config).direction()