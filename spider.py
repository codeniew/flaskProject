"""
爬取 微博/知乎/百度 热搜
"""
import json
import os
from datetime import datetime
from lxml import etree
import requests
import utils

BASE_URL = 'https://s.weibo.com'
JSON_DIR = './raw/weibo'
ARCHIVE_DIR = './archives'

BAIDU_BASE_URL = 'https://top.baidu.com'
BAIDU_JSON_DIR = './raw/baidu'
ZHIHU_JSON_DIR = './raw/zhihu'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 ' \
             'Safari/537.36 '
COOKIE = 'SUB=_2AkMVWDYUf8NxqwJRmP0Sz2_hZYt2zw_EieKjBMfPJ' \
         'RMxHRl-yj9jqkBStRB6PtgY-38i0AF7nDAv8HdY1ZwT3Rv8B5e5; ' \
         'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFencmWZyNhNlrzI6f0SiqP '


def get_zhihu_html(url):
    """ 获取网页 HTML 返回字符串
    Args:
        url: str, 网页网址
    Returns:
        HTML 字符串
    """
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    return response.text


def process_zhihu_html(content):
    """ 使用 xpath 解析 HTML, 提取榜单信息

    Args:
        content: str, 待解析的 HTML 字符串
    Returns:
        榜单信息的字典 字典(为了更容易写成json)
    """
    html = etree.HTML(content)

    script = html.xpath('//script[@id="js-initialData"]/text()')[0]
    items = json.loads(script)['initialState']['topstory']['hotList']
    rank = {
        item['target']['titleArea']['text']: {
            'href': item['target']['link']['url'],
            'hot': item['target']['metricsArea']['text'],
        }
        for item in items
    }
    return rank


def get_baidu_html(url):
    """ 获取网页 HTML 返回字符串

    Args:
        url: str, 网页网址
    Returns:
        HTML 字符串
    """
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


# 使用 xpath 解析 HTML
def process_baidu_html(content):
    """ 使用 xpath 解析 HTML, 提取榜单信息

    Args:
        content: str, 待解析的 HTML 字符串
    Returns:
        榜单信息的字典 字典
    """
    html = etree.HTML(content)
    titles = html.xpath('//html/body/div/div/main/div[2]/div/div[2]'
                        '/div[position()>1]/div[2]/a/div[1]/text()')
    hrefs = html.xpath('//html/body/div/div/main/div[2]/div/div[2]'
                       '/div[position()>1]/div[2]/a/@href')
    hots = html.xpath('//html/body/div/div/main/div[2]/div/div[2]'
                      '/div[position()>1]/div[1]/div[2]/text()')
    titles = [title.strip() for title in titles]
    hrefs = [href.strip() for href in hrefs]
    hots = [int(hot.strip()) for hot in hots]
    rank = {}
    for i, title in enumerate(titles):
        rank[title] = {'href': hrefs[i], 'hot': hots[i]}
    return rank


def get_html(url):
    """ 获取网页 HTML 返回字符串

    Args:
        url: str, 网页网址
    Returns:
        HTML 字符串
    """
    # Cookie 有效期至2023-02-10
    headers = {
        'User-Agent': USER_AGENT,
        'Cookie': COOKIE}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


# 使用 xpath 解析 HTML
def process_html(content):
    """ 使用 xpath 解析 HTML, 提取榜单信息

    Args:
        content: str, 待解析的 HTML 字符串
    Returns:
        榜单信息的字典 字典
    """
    html = etree.HTML(content)
    titles = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]'
        '/a[not(contains(@href, "javascript:void(0);"))]/text()')
    hrefs = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]'
        '/a[not(contains(@href, "javascript:void(0);"))]/@href')
    hots = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]'
        '/a[not(contains(@href, "javascript:void(0);"))]/../span/text()')
    titles = [title.strip() for title in titles]
    hrefs = [BASE_URL + href.strip() for href in hrefs]
    hots = [int(hot.strip().split(' ')[-1])
            for hot in hots]  # 该处除了热度还会返回大致分类，形如 `剧集 53412536`，前为分类，后为热度

    hot_data = {}
    for i, title in enumerate(titles):
        hot_data[title] = {'href': hrefs[i], 'hot': hots[i]}

    return hot_data


# 更新本日榜单
def update_json(json_dir, hot_data):
    """ 更新当天的 JSON 文件

    Args:
        hot_data: dict, 最新的榜单信息
    Returns:
        与当天历史榜单对比去重, 排序后的榜单信息字典
        :param hot_data:
        :param json_dir:
    """
    file_name = datetime.today().strftime('%Y%m%d') + '.json'
    file_name = os.path.join(json_dir, file_name)

    # 文件不存在则创建
    if not os.path.exists(file_name):
        utils.save(file_name, {})

    history_data = json.loads(utils.load(file_name))
    for k, value in hot_data.items():
        # 若当前榜单和历史榜单有重复的，取热度数值(名称后面的数值)更大的一个
        if k in history_data:
            history_data[k]['hot'] = max(
                history_data[k]['hot'], hot_data[k]['hot'])
        # 若没有，则添加
        else:
            history_data[k] = value

    # 将榜单按 hot 值排序

    if json_dir == './raw/zhihu':
        rank = dict(sorted(history_data.items(),
                           key=lambda item: int(item[1]['hot'].split()[0]), reverse=True))
    else:
        rank = dict(sorted(history_data.items(),
                           key=lambda item: item[1]['hot'], reverse=True))

    # 更新当天榜单 json 文件
    utils.save(file_name, rank)
    return rank


def main():
    """
    :return: 生成并更新微博/百度/知乎json文件
    """
    weibo_content = get_html(BASE_URL + '/top/summary')
    hot_data = process_html(weibo_content)
    update_json(JSON_DIR, hot_data)

    baidu_content = get_baidu_html(BAIDU_BASE_URL + '/buzz?b=1')
    baidu_hot_data = process_baidu_html(baidu_content)
    update_json(BAIDU_JSON_DIR, baidu_hot_data)

    zhihu_content = get_zhihu_html('https://www.zhihu.com/billboard')
    zhihu_hot_data = process_zhihu_html(zhihu_content)
    update_json(ZHIHU_JSON_DIR, zhihu_hot_data)

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "文件更新成功")


if __name__ == '__main__':
    main()
