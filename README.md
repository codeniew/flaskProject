# flaskProject

为spider.sh 添加权限 chmod -x spider.sh
crontab -e 添加定时任务
每隔60分钟更新一次文件
*/60 * * * * /home/ubuntu/venvpy/flaskProject/spider.sh

爬取 微博 知乎 百度 热搜
