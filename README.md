# Nao
Summer Course Project

## 主要功能
- 人脸识别：人脸检测，根据人脸说出人名
- 聊天：训练中文聊天语料库（暂定）/使用aiml公开的英文数据库
- 智能问答：基于搜索引擎的问答，提取百度和必应中的相关数据
- 指令执行：根据不同的指令做出相应的动作

## 文件结构
- conversation文件下是针对聊天使用的aiml语料库
- pics中保存Nao机器人拍摄的图片
- sound中存储Nao机器人记录的声音
- tools中为爬虫、分词等工具的代码
- naoMotion.py封装了Nao机器人的底层接口

## 测试相关
修改test.py中的代码，针对不同功能进行测试
``` python test.py ’Nao机器人的ip地址‘```
