# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/codesnap/blob/master/NOTICE.txt

from .htmlconverter import snap_tree_node_html, snap_tree_root_node_html, generate_html_report_from_snap_tree


class SnapTreeNode:
    def __init__(self, parent, name, t_entry, t_exit):
        self.parent = parent
        self.function_name = name   # 函数/类名称
        self.t_entry = t_entry   # 开始时间戳
        self.t_exit = t_exit   # 没搞懂赋值个0干啥
        self.exited = False
        self.children = []

    def html(self, parent_entry=None, parent_exit=None):
        """
        引用htmlconverter.py中snap_tree_node_html、snap_tree_root_node_html函数.
        为每一个节点生成html代码.
        """
        if parent_entry is None and parent_exit is None:
            # This is root
            return snap_tree_root_node_html(self)
        elif self.exited:
            return snap_tree_node_html(self, parent_entry, parent_exit)
        else:
            return ""


class SnapTree:
    """
    实现了一个 树 数据结构.
    因为buffer中的数据是call call call ... return return return这样形式的.
    因此在遍历buffer时, 一层一层往下add_entry建立新节点添加其name, time_begin, 在一层层往上add_exit为每一个相对应的节点添加其time_end.
    最终调用generate_html_report传入解析树(SnapTree)生成html代码并一层层传至CodeSnap的save方法.
    """
    def __init__(self):
        # 建立一个根节点
        self.root = SnapTreeNode(None, "__root__", 0, 0)
        # 当前节点暂时指向根节点
        self.curr = self.root
        self.end = 0

    def add_entry(self, name, t):
        # 当一个call 相关信息传入时建立新节点, 传入名称以及时间戳
        node = SnapTreeNode(self.curr, name, t, 0)
        # 将新节点中添加至其父节点
        self.curr.children.append(node)
        # 改变当前节点的指向
        self.curr = node
        if self.root.t_entry == 0:
            self.root.t_entry = t

    def add_exit(self, name, t):
        # 当一个return 相关信息传入时, 为当前节点的t_exit赋值t时间戳
        self.curr.t_exit = t
        if self.curr == self.root:
            # If we are out of the first stack, just ignore
            # This will actually help the exit of start() function
            return
        if name != self.curr.function_name:
            raise Exception("Function Entry/Exit did not match. {} vs {}".format(name, self.curr.function_name))
        self.curr.exited = True
        # 改变当前节点指向, 回到上一层其父节点.
        self.curr = self.curr.parent
        if t > self.root.t_exit:
            self.root.t_exit = t

    def generate_html_report(self):
        return generate_html_report_from_snap_tree(self)
