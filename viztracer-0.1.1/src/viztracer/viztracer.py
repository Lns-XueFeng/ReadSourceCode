# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt

from .tracer import _VizTracer


# This is the interface of the package. Almost all user should use this
# class for the functions
class VizTracer(_VizTracer):
    def __init__(self, tracer="c", verbose=1, max_stack_depth=-1, include_files=None, exclude_files=None):
        super().__init__(
                tracer=tracer,
                max_stack_depth=max_stack_depth,
                include_files=include_files,
                exclude_files=exclude_files
        )
        self.verbose = verbose   # 修改其父类的verbose

    def run(self, command, output_file="./result.html"):
        self.start()
        exec(command)
        self.stop()
        self.save()

    def save(self, output_file="./result.html"):
        if not self.parsed:
            self.parse()
        file_type = output_file.split(".")[-1]
        if file_type == "html":
            with open(output_file, "w") as f:
                f.write(self.generate_report())
        elif file_type == "json":
            with open(output_file, "w") as f:
                f.write(self.generate_json())
        else:
            raise Exception("Only html and json are supported")
