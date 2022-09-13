# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt

import sys
import argparse
from . import VizTracer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracer", nargs="?", choices=["c", "python"], default="c")
    parser.add_argument("--output_file", "-o", nargs="?", default="result.html")
    # 相较于前一个版本增加了一些命令
    parser.add_argument("--quiet", action="store_true", default=False)   # 可选参数：控制是否进行文字提示
    parser.add_argument("--max_stack_depth", nargs="?", type=int, default=-1)   # 可选参数：设置显示/记录调用最大栈数
    parser.add_argument("--exclude_files", nargs="*", default=None)   # 可选参数：暂时不懂其作用
    parser.add_argument("--include_files", nargs="*", default=None)   # 可选参数：暂时不懂其作用
    parser.add_argument("--run", nargs="*", default=[])

    parser.add_argument("command", nargs=argparse.REMAINDER)
    options = parser.parse_args(sys.argv[1:])

    # command = None   预先定义一个command变量较好
    if options.command:
        command = options.command
    elif options.run:
        command = options.run
    else:
        parser.print_help()
        exit(0)

    try:
        f = command[0]
        code_string = open(f).read()
    except FileNotFoundError:
        print("No such file as {}".format(f))
        exit(1)
    sys.argv = command[1:]

    # verbose控制是否进行文字提示
    if options.quiet:
        verbose = 0
    else:
        verbose = 1

    # 实例化VizTracer：通过命令启动__main__.py来运行VizTracer
    tracer = VizTracer(
        tracer=options.tracer, 
        verbose=verbose,
        max_stack_depth=options.max_stack_depth,   # 如果有设置, 否则None
        exclude_files=options.exclude_files,   # 如果有设置, 否则None
        include_files=options.include_files   # 如果有设置, 否则None
    )
    tracer.start()
    exec(code_string)
    tracer.stop()
    tracer.save(output_file=options.output_file)
