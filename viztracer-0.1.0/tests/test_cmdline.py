import unittest
import subprocess
import os


file_content = \
    """
    def fib(n):
        if n < 2:
            return 1
        return fib(n-1) + fib(n-2)
    fib(5)
    """


class TestCommandLineBasic(unittest.TestCase):

    def build_script(self):
        """创建一个fib代码文件用于测试"""
        with open("cmdline_test.py", "w") as f:
            f.write(file_content)

    def cleanup(self, output_file="result.html"):
        """测试完以后移除测试代码文件"""
        os.remove("cmdline_test.py")
        os.remove(output_file)

    def template(self, cmd_list, expected_output_file="result.html", success=True):
        self.build_script()   # 创建一个代码文件用于测试文件
        result = subprocess.run(cmd_list)   # 创建一个子进程执行cmd_list命令
        # 异或 (result.returncode != 0) -> False => (success ^ (result.returncode != 0)) -> True
        self.assertTrue(success ^ (result.returncode != 0))
        # 验证是否生成了相应的expected_output_file文件
        self.assertTrue(os.path.exists(expected_output_file))
        # 测试完清理一下
        self.cleanup(output_file=expected_output_file)

    def test_run(self):
        # 测试一下整个程序运行情况
        self.template(["python", "-m", "codesnap", "cmdline_test.py"])
    
    def test_outputfile(self):
        """测试程序的 不同命令 输出不同文件 情况"""

        # -o == --output_file
        self.template(
            ["python", "-m", "codesnap", "-o", "result.html", "cmdline_test.py"]
        )
        self.template(
            ["python", "-m", "codesnap", "-o", "result.json", "cmdline_test.py"],
            expected_output_file="result.json"
        )
        self.template(
            ["python", "-m", "codesnap", "--output_file", "result.html", "cmdline_test.py"]
        )
        self.template(
            ["python", "-m", "codesnap", "--output_file", "result.json", "cmdline_test.py"],
            expected_output_file="result.json"
        )
    
    def test_tracer(self):
        """测试不同tracer的运行情况, 有python和c的"""
        self.template(["python", "-m", "codesnap", "--tracer", "c", "cmdline_test.py"])
        self.template(["python", "-m", "codesnap", "--tracer", "python", "cmdline_test.py"])
