from fontTools.misc.visitor import Visitor
import pytest


class A:
    def __init__(self):
        self.a = 1
        self.b = [2, 3]
        self.c = {4: 5, 6: 7}
        self._d = 8
        self.e = 9
        self.f = 10


class B:
    def __init__(self):
        self.a = A()


class TestVisitor(Visitor):
    def __init__(self):
        self.value = []

    def _add(self, s):
        self.value.append(s)

    def visitLeaf(self, obj):
        self._add(obj)
        super().visitLeaf(obj)


@TestVisitor.register(A)
def visit(self, obj):
    self._add("A")


@TestVisitor.register_attrs([(A, "e")])
def visit(self, obj, attr, value):
    self._add(attr)
    self._add(value)
    return False


@TestVisitor.register(B)
def visit(self, obj):
    self._add("B")
    self.visitObject(obj)
    return False


@TestVisitor.register_attr(B, "a")
def visit(self, obj, attr, value):
    self._add("B a")


class VisitorTest(object):
    def test_visitor(self):
        b = B()
        visitor = TestVisitor()
        visitor.visit(b)
        assert visitor.value == ["B", "B a", "A", 1, 2, 3, 5, 7, "e", 9, 10]
