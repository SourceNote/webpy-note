# coding:utf-8
"""Python 2.3 兼容处理

这份代码值得学习的地方在于怎样实现threading.local
threading.local是用来实现线程安全的

"""
import threading


class threadlocal(object):
    """兼容python2.3：实现threading.local
    """

    def __getattribute__(self, name):
        if name == "__dict__":
            return threadlocal._getd(self)
        else:
            try:
                return object.__getattribute__(self, name)
            except AttributeError:
                try:
                    return self.__dict__[name]
                except KeyError:
                    raise AttributeError, name

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __delattr__(self, name):
        try:
            del self.__dict__[name]
        except KeyError:
            raise AttributeError, name

    def _getd(self):
        t = threading.currentThread()
        if not hasattr(t, '_d'):
            # 使用线程的__dict__用作线程本地存储
            t._d = {}

        _id = id(self)
        # 可以有多个threadlocal实例.
        # 使用id(self) 作为键值
        if _id not in t._d:
            t._d[_id] = {}
        return t._d[_id]


if __name__ == '__main__':
    d = threadlocal()
    d.x = 1
    print d.__dict__
    print d.x
