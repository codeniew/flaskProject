from datetime import datetime
import json
import os
import re

from lxml import etree
import requests

import utils

BASE_URL = 'https://s.weibo.com'
JSON_DIR = './raw/weibo'
ARCHIVE_DIR = './archives'

BAIDU_BASE_URL = 'https://top.baidu.com'
BAIDU_JSON_DIR = './raw/baidu'


def getHTML(url):
    """ 获取网页 HTML 返回字符串

    Args:
        url: str, 网页网址
    Returns:
        HTML 字符串
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.125 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    print(response.text)
    with open('test.html', 'w') as f:
        f.write(response.text)
    return response.text


# 使用 xpath 解析 HTML
def parseHTMLByXPath(content):
    """ 使用 xpath 解析 HTML, 提取榜单信息

    Args:
        content: str, 待解析的 HTML 字符串
    Returns:
        榜单信息的字典 字典
    """
    html = etree.HTML(content)

    titles = html.xpath('//html/body/div/div/main/div[2]/div/div[2]/div[position()>1]/div[2]/a/div[1]/text()')
    print(titles)
    print(len(titles))
    hrefs = html.xpath('//html/body/div/div/main/div[2]/div/div[2]/div[position()>1]/div[2]/a/@href')
    print(hrefs)
    hots = html.xpath('//html/body/div/div/main/div[2]/div/div[2]/div[position()>1]/div[1]/div[2]/text()')
    print(hots)
    titles = [title.strip() for title in titles]
    hrefs = [href.strip() for href in hrefs]
    hots = [int(hot.strip()) for hot in hots]

    correntRank = {}
    for i, title in enumerate(titles):
        correntRank[title] = {'href': hrefs[i], 'hot': hots[i]}
    print(correntRank)
    return correntRank


def get_html(url):
    """ 获取网页 HTML 返回字符串

    Args:
        url: str, 网页网址
    Returns:
        HTML 字符串
    """
    # Cookie 有效期至2023-02-10
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/84.0.4147.125 Safari/537.36',
        'Cookie': 'SUB=_2AkMVWDYUf8NxqwJRmP0Sz2_hZYt2zw_EieKjBMfPJRMxHRl-yj9jqkBStRB6PtgY-38i0AF7nDAv8HdY1ZwT3Rv8B5e5'
                  '; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFencmWZyNhNlrzI6f0SiqP '
    }
    response = requests.get(url, headers=headers)
    if response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding if response.apparent_encoding != 'ISO-8859-1' else 'utf-8'
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
        '//tr[position()>1]/td[@class="td-02"]/a[not(contains(@href, "javascript:void(0);"))]/text()')
    hrefs = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]/a[not(contains(@href, "javascript:void(0);"))]/@href')
    hots = html.xpath(
        '//tr[position()>1]/td[@class="td-02"]/a[not(contains(@href, "javascript:void(0);"))]/../span/text()')
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
    for k, v in hot_data.items():
        # 若当前榜单和历史榜单有重复的，取热度数值(名称后面的数值)更大的一个
        if k in history_data:
            history_data[k]['hot'] = max(
                history_data[k]['hot'], hot_data[k]['hot'])
        # 若没有，则添加
        else:
            history_data[k] = v

    # 将榜单按 hot 值排序
    rank = {k: v for k, v in sorted(
        history_data.items(), key=lambda item: item[1]['hot'], reverse=True)}

    # 更新当天榜单 json 文件
    utils.save(file_name, rank)
    return rank


# def updateReadme(rank):
#     """ 更新 README.md
#
#     Args:
#         rank: dict, 榜单信息
#     Returns:
#         None
#     """
#     filename = './README.md'
#
#     line = '1. [{title}]({href}) {hot}'
#     lines = [line.format(title=k, hot=v['hot'], href=v['href'])
#              for k, v in rank.items()]
#     rank = '\n'.join(lines)
#
#     rank = '最后更新时间 {}\n\n'.format(
#         datetime.now().strftime('%Y-%m-%d %X')) + rank
#     rank = '<!-- Rank Begin -->\n\n' + rank + '\n<!-- Rank End -->'
#
#     content = re.sub(
#         r'<!-- Rank Begin -->[\s\S]*<!-- Rank End -->', rank, utils.load(filename))
#     utils.save(filename, content)


def main():
    content = get_html(BASE_URL + '/top/summary')
    hot_data = process_html(content)
    update_json(JSON_DIR, hot_data)

    baidu_content = getHTML(BAIDU_BASE_URL + '/buzz?b=1')
    baidu_hot_data = parseHTMLByXPath(baidu_content)
    update_json(BAIDU_JSON_DIR, baidu_hot_data)
    # updateReadme(hot_json)


if __name__ == '__main__':
    main()
