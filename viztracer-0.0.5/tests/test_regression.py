import unittest
import codesnap


class TestIssue1(unittest.TestCase):
    """
    这个测试在干什么？
    不懂 不懂 不懂
    """
    def test_datetime(self):
        snap = codesnap.CodeSnap()
        snap.start()
        from datetime import timedelta
        timedelta(hours=5)
        snap.stop()
        snap.parse()
        snap.generate_json()
