# cmdManage--服务器命令管理工具  
[![Travis](https://img.shields.io/badge/release-1.0-brightgreen.svg)]()  [![Travis](https://img.shields.io/badge/build-passing-brightgreen.svg)]() [![Travis](https://img.shields.io/badge/developing-1.1-brightgreen.svg)]() [![Travis](https://img.shields.io/badge/python-2.7.10-brightgreen.svg)]()  
## 功能描述 
---
当项目要上测试服务器进行测试，或者项目上线之前要对新的服务器进行配置时。常常要安装一大堆的东西，redis、mysql等等。  
这些配置经常搞的我们焦头烂额。  
这个工具可以方便地管理经常用到的命令。  
只要打开目标服务器的ssh端口，在setting.yaml文件中稍微一配置，即可轻松管理。  
你既可以在工具中自定义命令，也可以使用已经封装好的。下面来看一个配置redis集群的例子。  

1. 在 resource/setting.yaml中修改pattern属性为RedisCluster (表面我们需要一个RedisCluster) 
2. 修改clusterInfo-slave 为 1 (给每个主节点分配一个从节点)
3. 然后根据需要修改settingInfo属性。   
4. 运行 src下的Main.py  
**注意集群实例数量必须大于等于6个**     
## 运行环境
---
windows 下请安装[openssl](https://www.openssl.org/)  
mac、和发行版本的linux请确定安装了ssh工具  
程序开发测试是在[![Travis](https://img.shields.io/badge/python-2.7.10-brightgreen.svg)]()版本下  
3.x版本没有经过测试  
## 项目结构
---
```
.
├── resource
│   ├── bootstrap.yaml        #不需要经常修改的配置
│   ├── clusterConfig.text    #rediscluster的配置文件
│   ├── setting.yaml          #根据需要修改配置文件
├── src
│   ├── AbsCallBack.py #       # 回调函数的抽象类
│   ├── AbsCmdFactory.py       # 命令工厂的抽象类
│   ├── AbsDirectiver.py       # 组装模块的抽象类
│   ├── AbsRun.py              # 实际运行时各个模块如何配合的抽象类
│   ├── AbsSSHConnect.py       # ssh链接远程服务器的抽象类
│   ├── DefaultDirectiver.py   # 默认的模块组装方式
│   ├── Main.py
│   ├── ParamFactory.py     # 生成在服务器上运行的命令
│   ├── ProInit.py          # 配置中心，主要加载在resource下的内容到内存
│   ├── RemoteException.py  #自定义错误
│   ├── ThreadingFactory.py # 线程工厂
│   ├── __init__.py
│   └── redisManage     # 封装好的redis集群命令。都是以上抽象类的实现
│       ├── RedisClusterCallBack.py
│       ├── RedisClusterCmdFactory.py
│       ├── RedisClusterRun.py
│       ├── RedisClusterRun.pyc
│       ├── RedisClusterSSHConnect.py
│       ├── __init__.py
```
## 历史版本
---
- developing 1.1(开发中)  
  TODO:  
  1. 支持自定义命令
  2. ProInit类setting可以接收多个地址 
  3. 支持从网络获取配置
- Release 1.0  
  支持RedisCluster 集群配置
## Licence  
---
