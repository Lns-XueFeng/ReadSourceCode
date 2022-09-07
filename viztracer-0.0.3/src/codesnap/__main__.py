# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt


"""
__main__.py -> 命令行运行 python -m package_name 时会启动这个文件作为程序的入口

浏览顺序：__main__.py -> codesnap.py -> tracer.py -> snaptree.py -> htmlconverter.py
类的情况：CodeSnap <- CodeSnapTracer - SnapTree - SnapTreeNode <- generate_html_report_from_snap_tree函数
htmlconverter.py 提供了几个函数来实现html的可视化展示, 并一层一层的传上来, 最终被暴露在CodeSnap的save函数中
"""


import sys
from . import CodeSnap

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m codesnap your_script_to_run.py [args]")
    try:
        # sys.argv = ['...\\__main__.py', 'your_script_to_run.py', ...]
        f = sys.argv[1]   # sys.argv[1] -> 'your_script_to_run.py'
        code_string = open(f).read()   # 拿到'your_script_to_run.py'代码字符串
    except FileNotFoundError:
        print("No such file as {}".format(f))
        exit(1)
    sys.argv.pop(0)
    snap = CodeSnap()   # Ctrl+鼠标左键 点击进入查看CodeSnap()的实现
    snap.start()
    exec(code_string)
    snap.stop()
    snap.save()
