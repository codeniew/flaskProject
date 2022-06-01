"""
单元测试
"""
import unittest


class MyTestCase(unittest.TestCase):
    """
    单元测试类
    """
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
