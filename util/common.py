class Common(object):
    def __init__(self):
        pass

    # 寻找各个Field的xpath规则共有的父节点
    @staticmethod
    def find_wrap(s1, s2):
        wrap = ''
        l1 = s1.split('/')
        l2 = s2.split('/')
        if len(l1) > len(l2):
            l = len(l2)
        else:
            l = len(l1)
        for i in range(0, l - 1):
            if l1[i] == l2[i]:
                wrap = wrap + l1[i] + '/'
            else:
                break

        return wrap[0:-1]

    @staticmethod
    def find_sub_of_wrap(wrap, str):
        temp = str[len(wrap)+1:]
        return './/' + temp