from datetime import date

import json

from flask import Flask, render_template

import spider

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    f = open('/home/nw/myPython/weibo-hot-search/raw/20220527.json')
    return f.read()


@app.route('/test')
def test():  # put application's code here
    return '跳转 test'


@app.route('/jinja')
def jinja():  # put application's code here
    spider.main()
    with open('./raw/weibo/'+date.today().strftime("%Y%m%d")+'.json', 'r') as f:
        data_weibo = json.load(f)
    with open('./raw/baidu/'+date.today().strftime("%Y%m%d")+'.json', 'r') as f:
        data_baidu = json.load(f)
    # print(data)

    navigation = []
    navigation2 = []
    for key, value in data_weibo.items():
        mydict = {}
        print(key, value)
        mydict['caption'] = key
        mydict['href'] = value['href']
        navigation.append(mydict)

    for key, value in data_baidu.items():
        mydict = {}
        print(key, value)
        mydict['caption'] = key
        mydict['href'] = value['href']
        navigation2.append(mydict)

    return render_template('jinja.html', navigation=navigation, navigation2=navigation2, a_variable='微博热搜')


if __name__ == '__main__':
    app.run()
