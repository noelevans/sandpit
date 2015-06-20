class Homogeneity(object):

    SAME = 's'    # eg "b b b b"
    MIX  = 'm'    # eg "a b a a"
    DIFF = 'd'    # eg "a b c d"

    @staticmethod
    def categorise(ul):
        if len(ul) == len(set(ul)):
            return DIFF
        if len(set(ul)) == 1:
            return SAME
        return MIX


if __name__ == '__main__':
    print Homogeneity.categorise([1, 1, 1])     # s
    print Homogeneity.categorise([1, 2, 3])     # d
    print Homogeneity.categorise([1, 1, 3])     # m
