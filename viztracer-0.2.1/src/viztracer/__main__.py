# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt

import sys
import argparse
from . import VizTracer
from . import FlameGraph


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracer", nargs="?", choices=["c", "python"], default="c")
    parser.add_argument("--output_file", "-o", nargs="?", default=None)
    parser.add_argument("--quiet", action="store_true", default=False)
    parser.add_argument("--max_stack_depth", nargs="?", type=int, default=-1)
    parser.add_argument("--exclude_files", nargs="*", default=None)
    parser.add_argument("--include_files", nargs="*", default=None)
    parser.add_argument("--ignore_c_function", action="store_true", default=False)
    # 新增可选参数 - 保存为火焰图
    parser.add_argument("--save_flamegraph", action="store_true", default=False)
    parser.add_argument("--generate_flamegraph", nargs="?", default=None)

    parser.add_argument("--run", nargs="*", default=[])
    parser.add_argument("command", nargs=argparse.REMAINDER)
    options = parser.parse_args(sys.argv[1:])

    if options.command:
        command = options.command
    elif options.run:
        command = options.run
    elif options.generate_flamegraph:
        flamegraph = FlameGraph()
        # options.generate_flamegraph -> my_script.py
        flamegraph.load(options.generate_flamegraph)
        if options.output_file:
            ofile = options.output_file
        else:
            ofile = "result_flamegraph.html"
        flamegraph.save(ofile)
        exit(0)
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
    if options.quiet:
        verbose = 0
    else:
        verbose = 1
    tracer = VizTracer(
        tracer=options.tracer,
        verbose=verbose,
        max_stack_depth=options.max_stack_depth,
        exclude_files=options.exclude_files,
        include_files=options.include_files,
        ignore_c_function=options.ignore_c_function
    )
    tracer.start()
    exec(code_string)
    tracer.stop()
    # save_flamegraph=options.save_flamegraph
    tracer.save(output_file=options.output_file, save_flamegraph=options.save_flamegraph)
