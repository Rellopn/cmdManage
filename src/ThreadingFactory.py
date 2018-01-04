# -*- coding: utf-8 -*-
import threading


class ThreadingFactory():
    """
        返回线程
    """

    def getThread(self, target, args):
        t = threading.Thread(target=target, args=args)
        t.setDaemon(True)
        return t
