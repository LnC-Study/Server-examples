class SingletonCreater(object):
    instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.instance :
            cls.instance = object.__new__(cls, *args, **kwargs)
        return cls.instance