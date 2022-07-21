"""
 flask 开始
"""
from datetime import date
import json
from flask import Flask, render_template
import spider

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    """
    :return: 网络热议首页
    """
    spider.main()
    with open('./raw/weibo/' + date.today().strftime("%Y%m%d") + '.json', 'r', encoding='utf-8') \
            as f_weibo:
        data_weibo = json.load(f_weibo)
    with open('./raw/baidu/' + date.today().strftime("%Y%m%d") + '.json', 'r', encoding='utf-8') \
            as f_baidu:
        data_baidu = json.load(f_baidu)
    with open('./raw/zhihu/' + date.today().strftime("%Y%m%d") + '.json', 'r', encoding='utf-8') \
            as f_zhihu:
        data_zhihu = json.load(f_zhihu)
    navigation = []
    navigation2 = []
    navigation_zhihu = []
    navigation = json_to_list(data_weibo, navigation)
    navigation2 = json_to_list(data_baidu, navigation2)
    navigation_zhihu = json_to_list(data_zhihu, navigation_zhihu)
    return render_template('jinri.html',
                           navigation=navigation,
                           navigation2=navigation2,
                           navigation_zhihu=navigation_zhihu)


def json_to_list(json_data, navigation):
    """将系统里面的 json 转化为 list
    :param json_data: json数据
    :param navigation: 初始list
    :return: new navigation
    """
    for key, value in json_data.items():
        my_dict = {'caption': key, 'href': value['href'], 'hot': value['hot']}
        navigation.append(my_dict)
    return navigation


if __name__ == '__main__':
    app.run()
