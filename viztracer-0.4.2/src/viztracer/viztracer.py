# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/viztracer/blob/master/NOTICE.txt

import os
import gzip
import multiprocessing
import sys
from .tracer import _VizTracer
from .flamegraph import FlameGraph
import viztracer.snaptrace


# This is the interface of the package. Almost all user should use this
# class for the functions
class VizTracer(_VizTracer):
    def __init__(self,
                 tracer="c",
                 verbose=1,
                 max_stack_depth=-1,
                 include_files=None,
                 exclude_files=None,
                 ignore_c_function=False,
                 log_return_value=False,
                 log_print=False,
                 pid_suffix=False,
                 output_file="result.html"):
        super().__init__(
                tracer=tracer,
                max_stack_depth=max_stack_depth,
                include_files=include_files,
                exclude_files=exclude_files,
                ignore_c_function=ignore_c_function,
                log_return_value=log_return_value,
                log_print=log_print
        )
        self.verbose = verbose
        self.pid_suffix = pid_suffix
        self.output_file = output_file
        self.system_print = None

    @property
    def verbose(self):
        return self.__verbose

    @verbose.setter
    def verbose(self, verbose):
        try:
            self.__verbose = int(verbose)
        except Exception:
            raise Exception("Verbose needs to be an integer, not {}".format(verbose))

    @property
    def pid_suffix(self):
        return self.__pid_suffix

    @pid_suffix.setter
    def pid_suffix(self, pid_suffix):
        try:
            self.__pid_suffix = int(pid_suffix)
        except Exception:
            raise Exception("pid_suffix needs to be a boolean, not {}".format(pid_suffix))

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, trace):
        self.stop()
        if type is None:
            self.save()

    def run(self, command, output_file=None):
        self.start()
        exec(command)
        self.stop()
        self.save(output_file)

    def save(self, output_file=None, save_flamegraph=False):
        if not self.parsed:
            self.parse()
        if output_file is None:
            output_file = self.output_file
        if self.pid_suffix:
            output_file_parts = output_file.split(".")
            output_file_parts[-2] = output_file_parts[-2] + "_" + str(os.getpid())
            output_file = ".".join(output_file_parts)
        file_type = output_file.split(".")[-1]
        if self.verbose > 0:
            print("Saving report to {}...".format(os.path.abspath(output_file)))
        if file_type == "html":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(self.generate_report())
        elif file_type == "json":
            data = self.generate_json(allow_binary=True)
            open_option = "wb" if type(data) is bytes else "w"
            with open(output_file, open_option) as f:
                f.write(data)
        elif file_type == "gz":
            data = self.generate_json(allow_binary=True)
            if type(data) is not bytes:
                data = data.encode("utf-8")
            with gzip.open(output_file, "wb") as f:
                f.write(data)
        else:
            raise Exception("Only html, json and gz are supported")

        if save_flamegraph:
            self.save_flamegraph(".".join(output_file.split(".")[:-1]) + "_flamegraph.html")

    def fork_save(self, output_file=None, save_flamegraph=False):
        if multiprocessing.get_start_method() != "fork":
            # You have to parse first if you are not forking, address space is not copied
            # Since it's not forking, we can't pickle tracer, just set it to None when
            # we spawn
            if not self.parsed:
                self.parse()
            tracer = self._tracer
            self._tracer = None
        else:
            # Fix the current pid so it won't give new pid when parsing
            self._tracer.setpid()

        p = multiprocessing.Process(target=self.save, daemon=False,
                                    kwargs={"output_file": os.path.abspath(output_file), "save_flamegraph": save_flamegraph})
        p.start()

        if multiprocessing.get_start_method() != "fork":
            self._tracer = tracer
        else:
            # Revert to the normal pid mode
            self._tracer.setpid(0)

    def save_flamegraph(self, output_file=None):
        flamegraph = FlameGraph(self.data)
        if output_file is None:
            name_list = self.output_file.split(".")
            output_file = ".".join(name_list[:-1]) + "_flamegraph." + name_list[-1]
        flamegraph.save(output_file)
