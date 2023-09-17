class Node:
    def __init__(self, value, children):
        self.value = value  # value of the node, can be int or str
        self.children = children  # list of Node

    def evaluate(self):
        return self.value


class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def evaluate(self):
        return self.value


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        if self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()

        if self.value == "-":
            return -self.children[0].evaluate()


class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self):
        return None
