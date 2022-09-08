# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt

from .htmlconverter import snap_tree_node_html, snap_tree_root_node_html, generate_html_report_from_snap_tree


class SnapTreeNode:
    def __init__(self, parent, name, t_entry, t_exit):
        self.parent = parent
        self.function_name = name
        self.t_entry = t_entry
        self.t_exit = t_exit
        self.exited = False
        self.children = []   # 可以使json_object方法的列表解析式向下遍历子节点

    def html(self, parent_entry=None, parent_exit=None):
        if parent_entry is None and parent_exit is None:
            # This is root
            return snap_tree_root_node_html(self)
        elif self.exited:
            return snap_tree_node_html(self, parent_entry, parent_exit)
        else:
            return ""
    
    def json_object(self):
        # 将相关信息存到字典中并返回
        data = {
            "name": self.function_name,   # 函数名
            "value": self.t_exit - self.t_entry,   # 持续时间
            "entry": self.t_entry,   # 开始时间戳
            "exit": self.t_exit,   # 结束时间戳
            # 递归遍历所有节点, 生成所有节点的相关数据
            "children": [child.json_object() for child in self.children]
        }

        return data


class SnapTree:
    def __init__(self):
        self.root = SnapTreeNode(None, "__root__", 0, 0)
        self.curr = self.root
        self.end = 0

    def add_entry(self, name, t):
        node = SnapTreeNode(self.curr, name, t, 0)
        self.curr.children.append(node)
        self.curr = node
        if self.root.t_entry == 0:
            self.root.t_entry = t

    def add_exit(self, name, t):
        self.curr.t_exit = t
        if self.curr == self.root:
            # If we are out of the first stack, just ignore
            # This will actually help the exit of start() function
            return
        if name != self.curr.function_name:
            raise Exception("Function Entry/Exit did not match. {} vs {}".format(name, self.curr.function_name))
        self.curr.exited = True
        self.curr = self.curr.parent
        if t > self.root.t_exit:
            self.root.t_exit = t

    def generate_html_report(self):
        return generate_html_report_from_snap_tree(self)

    def get_json(self):
        # 定位到SnapTreeCode
        return self.root.json_object()
