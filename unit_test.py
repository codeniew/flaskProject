"""
单元测试
"""
import unittest
import spider



class MyTestCase(unittest.TestCase):
    """
    单元测试类
    """
    def test_get_zhihu_html(self):
        """
        :return: 是否为空
        """
        self.assertIsNotNone(spider.get_zhihu_html('https://www.zhihu.com/billboard'))

    def test_get_html(self):
        """
        :return:抓取微博是否为空
        """
        self.assertIsNotNone(spider.get_html('https://s.weibo.com/top/summary'))

    def test_update_json(self):
        """测试 更新json文件"""
        filename = './raw/test'
        hot_data = {"测试": {"href": "baidu.com", "hot": "10000"}}
        self.assertIsNotNone(spider.update_json(filename, hot_data))

    def test_hot_sort(self):
        """测试热搜从高到低排序"""
        hot_data = {"测试1": {"href": "baidu.com", "hot": 10000},
                    "测试2": {"href": "baidu.com", "hot": 99},
                    "测试3": {"href": "baidu.com", "hot": 1000},
                    "测试4": {"href": "baidu.com", "hot": 900}}
        rank = spider.hot_sort('/raw/weibo', history_data=hot_data)
        for key, value in rank.items():
            print(value["hot"])
        self.assertIsNotNone(rank)


if __name__ == '__main__':
    unittest.main()
