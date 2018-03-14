#! /usr/bin/env python
# coding:utf-8
from threading import Thread


class MyThread(Thread):
    def __init__(self, func, args):
        Thread.__init__(self)
        self.func = func
        self.arg = arg
        self.result = None

    def run(self):
        self.result = self.func(self.arg)

    def get_result(self):
        return self.result

