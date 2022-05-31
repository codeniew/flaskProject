# -*- coding=utf-8 -*-

from datetime import datetime
import json
import os
import re

from lxml import etree
import requests

# import log_tools
import utils

# ZHIHU_JSON_DIR = './raw/zhihu'
#
# LOG_DIR = './logs'


# logger = log_tools.init_logger(__name__, log_path=LOG_DIR)


# def get_zhihu_html(url):
#     """ 获取网页 HTML 返回字符串
#
#     Args:
#         url: str, 网页网址
#     Returns:
#         HTML 字符串
#     """
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/84.0.4147.125 Safari/537.36 '
#     }
#     response = requests.get(url, headers=headers)
#     return response.text
#
#
# # 使用 xpath 解析 HTML
# def process_zhihu_html(content):
#     """ 使用 xpath 解析 HTML, 提取榜单信息
#
#     Args:
#         content: str, 待解析的 HTML 字符串
#     Returns:
#         榜单信息的字典 字典(为了更容易写成json)
#     """
#     html = etree.HTML(content)
#
#     script = html.xpath('//script[@id="js-initialData"]/text()')[0]
#     print(script)
#     items = json.loads(script)['initialState']['topstory']['hotList']
#     print(items)
#     rank = {
#         item['target']['titleArea']['text']: {
#             'hrefs': item['target']['link']['url'],
#             'hot': item['target']['metricsArea']['text'],
#         }
#         for item in items
#     }
#     return rank


# 更新本日榜单
# def updateJSON(correntRank):
#     ''' 更新当天的 JSON 文件
#
#     Args:
#         correntRank: dict, 最新的榜单信息
#     Returns:
#         与当天历史榜单对比去重, 排序后的榜单信息字典
#     '''
#     filename = datetime.today().strftime('%Y%m%d') + '.json'
#     filename = os.path.join(ZHIHU_JSON_DIR, filename)
#
#     # 文件不存在则创建
#     if not os.path.exists(filename):
#         utils.save(filename, {})
#
#     historyRank = json.loads(utils.load(filename))
#     for k, v in correntRank.items():
#         # 若当前榜单和历史榜单有重复的，取热度更高的一个
#         if k in historyRank:
#             if int(historyRank[k]['hot'].split()[0]) < int(correntRank[k]['hot'].split()[0]):
#                 historyRank[k]['hot'] = correntRank[k]['hot']
#         # 若没有，则添加
#         else:
#             historyRank[k] = v
#
#     # 将榜单按 hot 值排序
#     rank = {k: v for k, v in sorted(historyRank.items(), key=lambda item: int(item[1]['hot'].split()[0]), reverse=True)}
#
#     # 更新当天榜单 json 文件
#     utils.save(filename, rank)
#     return rank



#
# def main():
#     try:
#         content = get_zhihu_html('https://www.zhihu.com/billboard')
#         correntRank = process_zhihu_html(content)
#         rankJSON = updateJSON(correntRank)
#         # rankMD = updateArchive(rankJSON)
#         # updateReadme(rankMD)
#     except Exception as e:
#         # logger.exception(e)
#         raise e
#
#
# if __name__ == '__main__':
#     main()
