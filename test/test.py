class A:
    def __init__(self):
        self.li = [1, 2, 3]
        self.count = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= len(self.li) - 1:
            raise StopIteration
        self.count += 1
        return self.li[self.count]


for i in A():
    print(i)


def generate():
    li = [1, 2, 3]
    for _ in li:
        yield _


def pipe_(s):
    for i in s:
        if issubclass(i.__class__, int):
            yield str(i)
        else:
            raise TypeError


g = pipe_(generate())

print(list(g))

p = {True: "嘿嘿嘿", 1: "哈哈哈", 1.0: "呵呵呵"}
print(p)

print(True == 1 == 1.0)

print(hash(True), hash(1), hash(1.0))

print(id(True), id(1), id(1.0))
