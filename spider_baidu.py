# # -*- coding=utf-8 -*-
#
# from datetime import datetime
# import json
# import os
# import re
#
# from lxml import etree
# import requests
#
# # import log_tools
# import utils
#
# BAIDU_BASE_URL = 'https://top.baidu.com'
# BAIDU_JSON_DIR = './raw/baidu'
#
#
# def getHTML(url):
#     """ 获取网页 HTML 返回字符串
#
#     Args:
#         url: str, 网页网址
#     Returns:
#         HTML 字符串
#     """
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)
#
#     # 百度专属，百度 永远的拉胯之神 [/裂开]
#     response.encoding = 'utf-8'
#     # response.encoding = 'gb2312'
#     #
#     # if response.encoding == 'ISO-8859-1':
#     #     response.encoding = response.apparent_encoding if response.apparent_encoding != 'ISO-8859-1' else 'utf-8'
#
#     print(response.text)
#     with open('test.html', 'w') as f:
#         f.write(response.text)
#     return response.text
#
#
# # 使用 xpath 解析 HTML
# def parseHTMLByXPath(content):
#     """ 使用 xpath 解析 HTML, 提取榜单信息
#
#     Args:
#         content: str, 待解析的 HTML 字符串
#     Returns:
#         榜单信息的字典 字典
#     """
#     html = etree.HTML(content)
#
#     titles = html.xpath('//html/body/div/div/main/div[2]/div/div[2]/div[position()>1]/div[2]/a/div[1]/text()')
#     print(titles)
#     print(len(titles))
#     hrefs = html.xpath('//html/body/div/div/main/div[2]/div/div[2]/div[position()>1]/div[2]/a/@href')
#     print(hrefs)
#     hots = html.xpath('//html/body/div/div/main/div[2]/div/div[2]/div[position()>1]/div[1]/div[2]/text()')
#     print(hots)
#     titles = [title.strip() for title in titles]
#     hrefs = [href.strip() for href in hrefs]
#     hots = [int(hot.strip()) for hot in hots]
#
#     correntRank = {}
#     for i, title in enumerate(titles):
#         correntRank[title] = {'href': hrefs[i], 'hot': hots[i]}
#     print(correntRank)
#     return correntRank
#
#
# # 更新本日榜单
# def updateJSON(correntRank):
#     """ 更新当天的 JSON 文件
#
#     Args:
#         correntRank: dict, 最新的榜单信息
#     Returns:
#         与当天历史榜单对比去重, 排序后的榜单信息字典
#     """
#     filename = datetime.today().strftime('%Y%m%d') + '.json'
#     filename = os.path.join(BAIDU_JSON_DIR, filename)
#
#     # 文件不存在则创建
#     if not os.path.exists(filename):
#         utils.save(filename, {})
#
#     historyRank = json.loads(utils.load(filename))
#     for k, v in correntRank.items():
#         # 若当前榜单和历史榜单有重复的，取热度更高的一个
#         if k in historyRank:
#             historyRank[k]['hot'] = max(historyRank[k]['hot'], correntRank[k]['hot'])
#         # 若没有，则添加
#         else:
#             historyRank[k] = v
#
#     # 将榜单按 hot 值排序
#     rank = {k: v for k, v in sorted(historyRank.items(), key=lambda item: item[1]['hot'], reverse=True)}
#
#     # 更新当天榜单 json 文件
#     utils.save(filename, rank)
#     return rank
#
#
# # def updateArchive(rank):
# #     """ 更新当天的 Markdown 归档文件
# #
# #     Args:
# #         rank: dict, 榜单信息
# #     Returns:
# #         更新后当天 Markdown 文件内容
# #     """
# #     line = '1. [{title}]({href}) {hot}'
# #     lines = [line.format(title=k, hot=v['hot'], href=v['href']) for k, v in rank.items()]
# #     content = '\n'.join(lines)
# #
# #     filename = datetime.today().strftime('%Y%m%d') + '.md'
# #     filename = os.path.join(ARCHIVE_DIR, filename)
# #
# #     # 更新当天榜单 markdown 文件
# #     save(filename, content)
# #     return content
#
#
# # def updateReadme(rank):
# #     """ 更新 README.md
# #
# #     Args:
# #         rank: str, markdown 格式的榜单信息
# #     Returns:
# #         None
# #     """
# #     filename = './README.md'
# #
# #     rank = '最后更新时间 {}\n\n'.format(datetime.now().strftime('%Y-%m-%d %X')) + rank
# #     rank = '<!-- Rank Begin -->\n\n' + rank + '\n<!-- Rank End -->'
# #
# #     content = re.sub(r'<!-- Rank Begin -->[\s\S]*<!-- Rank End -->', rank, load(filename))
# #     save(filename, content)
#
#
# def main():
#     url = '/buzz?b=1'
#     try:
#         content = getHTML(BAIDU_BASE_URL + url)
#         correntRank = parseHTMLByXPath(content)
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