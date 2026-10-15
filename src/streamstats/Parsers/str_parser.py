class StripChars:
    def __init__(self, chars):
        self.__chars = chars

    def __call__(self, *args, **kwargs):
        if type(args[0]) is not str:
            raise TypeError("You passed to StrParser not string!")
        return args[0].strip(self.__chars)


class ReplaceChars:
    def __init__(self, chars):
        self.__chars = chars

    def __call__(self, *args, **kwargs):
        if type(args[0]) is not str:
            raise TypeError("You passed to StrParser not string!")
        cp = args[0]
        for i in self.__chars:
            cp = cp.replace(i, "")
        return cp
