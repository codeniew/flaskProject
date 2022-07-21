# flask_spider_Project

## 爬取 微博/知乎/百度 热搜
获取当天的热搜信息，每隔一小时更新一次，以json格式归档。

## 总体设计
### 防止热搜被撤

本项目可以按照按当天按热度进行排名。

### 后续计划
当数据量足够大的时候，可以对热搜数据进行分析。
## pyLint代码评估和改进
对代码进行规范的命名，为模块和方法添加注释

修改前：

    rank = {k: v for k, v in sorted(
        historyRank.items(), key=lambda item: item[1]['hot'], reverse=True)}
修改后：

        rank = dict(sorted(history_data.items(),
                           key=lambda item: item[1]['hot'], reverse=True))


Pylint: Module 'lxml.etree' has no 'HTML' member, 
but source is unavailable. 
Consider adding this module to extension-pkg-allow-list 
if you want to perform analysis based on run-time introspection of living objects

` pylint --generate-rcfile > .pylintrc`生成 .pylintrc 文件

将`extension-pkg-whitelist=lxml` 加入 .pylintrc


## 单元测试
。。。


### 定时任务
1. 为spider.sh 添加权限 `chmod -x spider.sh`
2. `crontab -e` 添加定时任务
3. 每隔60分钟更新一次文件
4. `*/60 * * * * /home/ubuntu/venvpy/flaskProject/spider.sh` 



