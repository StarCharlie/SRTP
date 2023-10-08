## 软件开发总体报告

### 1.项目介绍

##### 项目名称

中医艾灸可视化知识服务平台

##### 项目简介

本项目为浙江大学2022.5-2023.5 SRTP（大学生科研训练计划）项目【院级】作品。

本项目旨在制作艾灸知识的可视化平台，为大众提供艾灸的知识普及和相关指导。本项目通过爬虫技术，抓取中医艾灸的相关知识，将其通过NLP关系抽取以及Neo4j数据库存储构建成知识图谱，同时使用Vue+Flask的前后端分离方式制作平台网页。

本项目分为**主页展示、详情查看、用户搜索、知识图谱、用户中心**五大模块，各模块用不同的方式向用户介绍艾灸的**灸法、穴位、治疗病症**三大领域知识，模块之间关系密切，便于用户操作于切换，从而达到艾灸知识的充分可视化。

本项目侧重于艾灸的知识图谱构建，在获取大量数据后，通过信息筛查和信息抽取的技术，再进行融合与加工，制作成知识图谱。用户可根据自己的需求，在网页平台中挑选相对应的服务模块，而平台会根据事件触发，从知识图谱中挑选相关的信息并提供。

##### 技术栈

本项目采用了前后端分离的开发方式，前端使用Vue框架，并使用ElementUI+echarts作为组件库并辅助图展示，后端采用Python-flask框架。数据库则采用了关系型数据库MySQL与图数据库Neo4j。同时使用ElasticSearch辅助进行模糊搜索。

##### 开发人员

|  姓名  |  身份/主要工作   |
| :----: | :--------------: |
| 叶歌凡 |  组长、知识抽取  |
| 孙宇桐 | 组员、前后端开发 |
| 谢昕冉 |  组员、项目部署  |

##### 项目展示



### 2.开发环境

|   操作系统   |          Windows10          |                    /                     |
| :----------: | :-------------------------: | :--------------------------------------: |
|     描述     |            环境             |                官网/其它                 |
|   开发工具   | Visual Studio Code、PyCharm |                    /                     |
|   前端框架   |           Vue3.0            |          https://cn.vuejs.org/           |
|  UI组件框架  |        Element-plus         |   https://element-plus.gitee.io/zh-CN/   |
| 知识图谱展示 |           Echarts           | https://echarts.apache.org/zh/index.html |
|   后端框架   |        Python Flask         |          https://flask.net.cn/           |
| 搜索引擎支持 |     ElasticSearch 8.6.2     |        https://www.elastic.co/cn/        |
|  关系数据库  |          MySQL8.0           |          https://www.mysql.com/          |
|   图数据库   |         Neo4j 5.4.0         |            https://neo4j.com/            |

### 3.运行环境

#### 硬件支持

|   描述   |             环境              |
| :------: | :---------------------------: |
| 操作系统 | Windows8.0以上、MAC OS、Linux |
|   CPU    |         不小于2.0GHz          |
|   内存   |          不小于2.0GB          |

#### 软件依赖

|     描述     |            环境             |                官网/其它                 |
| :----------: | :-------------------------: | :--------------------------------------: |
|   操作系统   |     Windows8以上、Linux     |                    /                     |
|   开发工具   | Visual Studio Code、PyCharm |                    /                     |
|   前端框架   |           Vue3.0            |          https://cn.vuejs.org/           |
|  UI组件框架  |        Element-plus         |   https://element-plus.gitee.io/zh-CN/   |
| 知识图谱展示 |           Echarts           | https://echarts.apache.org/zh/index.html |
|   后端框架   |        Python Flask         |          https://flask.net.cn/           |
| 搜索引擎支持 |     ElasticSearch 8.6.2     |        https://www.elastic.co/cn/        |
|  关系数据库  |          MySQL8.0           |          https://www.mysql.com/          |
|   图数据库   |         Neo4j 5.4.0         |            https://neo4j.com/            |

### 4.部署方案

#### 前端

前端在本Github项目的Front分支中，请先通过以下git命令克隆相关文件

```
git clone https://github.com/StarCharlie/SRTP.git -b Front
```

此后，将得到对应文件，请按以下步骤操作

+ 进入/src/global/global.js中，修改以下代码

+ ```javascript
  const baseURL = "http://127.0.0.1:5000";	// 后端服务器地址
  const neo4jUserName = 'neo4j';				// Neo4j服务器用户名（请确保Neo4j注册完毕）
  const neo4jUserPassword = 'xxx';			// Neo4j服务器密码
  ```

+ 在根目录中，运行以下命令，启动程序

  ==安装依赖包==
  
  ```
  npm install
  ```
  
  ==启动程序==
  
  ```
  npm run serve
  ```
  
  网页将部署在对应端口（默认为8080），访问页面正常即可

#### 后端

后端在本Github项目的Server分支中，请先通过以下git命令克隆相关文件

```
git clone https://github.com/StarCharlie/SRTP.git -b server
```

此后，将得到对应文件，请按以下步骤操作

+ 新建一个venv解释器环境

+ 安装依赖库（下面推荐两种方式）

  + 使用pip命令安装以下依赖库：

    + |       名称       | 最低版本 |
      | :--------------: | :------: |
      |      Flask       |  2.2.5   |
      |    Flask-Cors    |  3.0.10  |
      | Flask-SQLAlchemy |  3.0.3   |
      |     PyMySQL      |  1.0.3   |
      |    SQLAlchemy    |  2.0.12  |
      |  elasticsearch   |  8.7.0   |
      |      numpy       |  1.21.6  |
      |      pandas      |  1.3.5   |
      |      py2neo      | 2021.2.3 |

  + 运行根目录下方的requirements.txt

    + ```powershell
      pip install -r requirement.txt
      ```

+ 进入/configs/config.py，修改以下信息

  ```python
  # MySQL
  DATABASE = 'aijiu'					# 你的对应数据库名称
  USERNAME = 'xxx'					# MySQL数据库用户名
  PASSWORD = 'xxx'					# MySQL数据库用户密码
  
  # Neo4j
  NEO4j_NAME = 'neo4j'				# Neo4j服务器用户名（请确保Neo4j注册完毕）
  NEO4j_PASS = 'xxx'					# Neo4j服务器用户密码（请确保Neo4j注册完毕）
  NEO4j_GRAPH = 'neo4j'				# Neo4j对应表名，默认为neo4j因此可以不用更改
  ```

+ 运行根目录下方的app.py，出现后端url即可

#### 数据库

数据库部署方式如下

+ MySQL

  + 在MySQL中新建一个数据库，命名方式要与后端的DATABASE相同
  + 在该库中注入static/datas/srtp.sql文件

  > #### .sql文件导入方式
  >
  > + 进入mysql
  > + use 数据库名称
  > + 执行 source name.sql
  >   + name.sql：要导出的.sql名称，请包含路径，例如D:\output.sql

+ Neo4j

  + 下载并安装Neo4j（**最低要求版本5.4.0**）
  + cmd进入到下载文件夹中bin目录中运行neo4j console，启动Neo4j
  + 到localhost:7474端口进行基本配置（初始用户名和密码都是neo4j）
  + 到config.py中配置Neo4j相关内容（把用户名和密码改了就好）
  + **运行后端根目录中的graphGenerated.py（生成初始图）**
  + 网页打开localhost:7474查看是否有生成对应图

#### 其它

ElasticSearch（模糊搜索辅助搜索引擎）配置方法如下：

+ 下载并安装ES（**最低版本要求8.2.6**）
+ 进入到bin文件夹中运行elasticsearch.bat文件启动es
+ 【注意：最好登录http://localhost:9200测试一下能否正常运行】
+ **启动后端**，网页访问（后端url/home/createES）生成索引，恢复结果为createES即代表建立索引成功
  + 例如后端建立在http://localhost:5000，则访问网页url为http://localhost:5000/home/createES



