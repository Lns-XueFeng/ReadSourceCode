# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt

import sys
import time
from .snaptree import SnapTree
import codesnap.snaptrace as snaptrace


class CodeSnapTracer:
    """
    CodeSnapTracer类为codesnap的核心实现
    """
    def __init__(self, tracer="python"):
        self.buffer = []   # 存储变量, 函数, 类等名称, 耗时等等
        self.enable = False
        self.parsed = False
        self.snaptree = SnapTree()   # 实例化了SnapTree类, 用来解析buffer中的数据
        self.tracer = tracer   # 默认使用了python sys.setprofile()来获取代码运行数据

    def start(self):
        """
        开启 sys.setprofile()
        """
        self.enable = True
        self.parsed = False
        if self.tracer == "python":
            sys.setprofile(self.tracefunc)   # 启动profiling跟踪函数
        elif self.tracer == "c":
            snaptrace.start()   # tracer C语言的实现

    def stop(self):
        """停止 sys.setprofile()"""
        self.enable = False
        if self.tracer == "python":
            sys.setprofile(None)   # 只需要传入None该方法便会自动停止
        elif self.tracer == "c":
            snaptrace.stop()

    def clear(self):
        """
        清空buffer
        """
        if self.tracer == "python":
            self.buffer = []
        elif self.tracer == "c":
            snaptrace.clear()
    
    def cleanup(self):
        if self.tracer == "c":
            snaptrace.cleanup()

    def tracefunc(self, frame, event, arg):
        """
        此函数会：call时调用一次, return也调用一次, 拿到相关代码信息
        # sys文档：https://docs.python.org/3/library/sys.html
        """
        if event == "call" or event == "return":
            f_locals = frame.f_locals
            if "self" in f_locals:
                # 判断CodeSnapTracer本身是否也在f_locals里面, 如果有, return忽略掉
                if issubclass(f_locals["self"].__class__, self.__class__):
                    # If we are inside this class, ignore
                    return
                # type(f_locals["self"]) == f_locals["self"].__class__
                class_name = type(f_locals["self"]).__name__ + "."
            else:
                class_name = ""

            # 可以看见这个时候获取的数据还比较简单, 仅仅就是filename, classname, func_name以及time
            if event == "call":
                name = "{}.{}{}".format(frame.f_code.co_filename, class_name, frame.f_code.co_name)
                self.buffer.append(("entry", name, time.perf_counter()))   # 元组形式
            elif event == "return":
                name = "{}.{}{}".format(frame.f_code.co_filename, class_name, frame.f_code.co_name)
                self.buffer.append(("exit", name, time.perf_counter()))

    def parse(self):
        total_entries = 0   # 用来做测试验证
        self.stop()   # 在解析之前一定要确认sys.setprofile()是停止的
        if not self.parsed:
            if self.tracer == "python":
                # 将buffer中的数据传给SnapTree
                for data in self.buffer:
                    if data[0] == "entry":
                        self.snaptree.add_entry(data[1], data[2])
                    elif data[0] == "exit":
                        self.snaptree.add_exit(data[1], data[2])
                    else:
                        raise Exception("Unexpected data type")
                    total_entries += 1
                self.buffer = []   # 解析完成之后清空buffer, 防止污染
            elif self.tracer == "c":
                buffer = snaptrace.load()
                for data in buffer:
                    # [type, ts, file_name, class_name, func_name]
                    # type is an integer, 0 for entry and 3 for exit
                    # class_name could be None
                    if data[3]:
                        name = ".".join([data[2], data[3], data[4]])
                    else:
                        name = ".".join([data[2], data[4]])
                    if data[0] == 0:
                        self.snaptree.add_entry(name, data[1])
                    elif data[0] == 3:
                        self.snaptree.add_exit(name, data[1])
                    else:
                        raise Exception("Unexpected data type")
                    total_entries += 1
            self.parsed = True
        if self.enable:
            self.start()

        return total_entries

    def generate_report(self):
        return self.snaptree.generate_html_report()
