# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt


"""
__init__.py 的存在使codesnap可以作为一个包从外部调用
例如：在此模块外部的py文件中可 from codesnap import CodeSnap ...

注意：不要直接运行模块内部的文件, 会发生相对路径相关的错误.
"""


from .tracer import CodeSnapTracer
from .codesnap import CodeSnap


# 允许外部访问的模块
__all__ = [
    "CodeSnapTracer",
    "CodeSnap"
]
