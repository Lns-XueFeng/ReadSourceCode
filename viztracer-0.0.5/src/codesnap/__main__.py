# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt

import sys
import argparse
from . import CodeSnap

if __name__ == '__main__':
    """
    usage: __main__.py [-h] [--tracer [{c,python}]] [--output_file [OUTPUT_FILE]] ...
    
    positional arguments:
      command
    
    optional arguments:
      -h, --help            show this help message and exit
      --tracer [{c,python}]
      --output_file [OUTPUT_FILE], -o [OUTPUT_FILE]
    """
    parser = argparse.ArgumentParser()
    # python -m codesnap --tracer python
    # 可选参数--tracer, nargs="?"表示如果有 将消耗一个参数, 默认default为c, 供选择的参数python c
    parser.add_argument("--tracer", nargs="?", choices=["c", "python"], default="c")
    # python -m codesnap -o或--output_file output.html
    # 可选参数--output_file或-o, nargs="?"表示如果有 将消耗一个参数, 默认default为result.html
    parser.add_argument("--output_file", "-o", nargs="?", default="result.html")
    # 位置参数 nargs=argparse.REMAINDER -> 不懂...
    # 可选参数的后面一般假设为位置参数
    parser.add_argument("command", nargs=argparse.REMAINDER)
    options = parser.parse_args(sys.argv[1:])
    try:
        # python -m codesnap your_script_to_run.py
        # python -m codesnap --tracer python your_script_to_run.py
        # python -m codesnap --output_file output.html your_script_to_run.py
        # python -m codesnap --output_file output.json your_script_to_run.py
        f = options.command[0]   # 拿到your_script_to_run.py的绝对路径
        code_string = open(f).read()   # 读取源代码
    except FileNotFoundError:
        print("No such file as {}".format(f))
        exit(1)
    sys.argv = options.command[1:]
    snap = CodeSnap(tracer=options.tracer)
    snap.start()
    exec(code_string)
    snap.stop()
    snap.save(output_file=options.output_file)
