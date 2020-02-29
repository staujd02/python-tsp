
class Vector(object):

    def __init__(self, arg1, arg2=None, arg3=None):
        self.data = ['', '', 0]
        if arg2 == None or arg3 == None:
            self.__cloneVector(arg1)
        else:
            self.__createNewVector(arg1, arg2, arg3)

    def __cloneVector(self, vector):
        self.__createNewVector(vector[0], vector[1], vector[2])

    def __createNewVector(self, start, end, length):
        self.data[0] = str(start)
        self.data[1] = str(end)
        self.data[2] = length

    def isEqual(self, vector):
        return vector.data == self.data

    def __str__(self):
        return "<" + self.data[0] + "->" + self.data[1] + ":" + str(self.data[2]) + ">"

    def __unicode__(self):
        return u"<" + self.data[0] + "->" + self.data[1] + ":" + str(self.data[2]) + ">"

    def __getitem__(self, i):
        return self.data[i]

    def __delitem__(self, i):
        del self.data[i]

    def __setitem__(self, i, value):
        self.data[i] = value
    
    def __eq__(self, other):
        return self.data[2] == other.data[2]

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.data[2] < other.data[2]

    def __le__(self, other):
        return self.data[2] <= other.data[2]

    def  __gt__(self, other):
        return self.data[2] > other.data[2]

    def __ge__(self, other):
        return self.data[2] >= other.data[2]

class NoOpCompare(object):
    def __eq__(self, other):
        return 0
    def __ne__(self, other):
        return 0
    def __lt__(self, other):
        return 0
    def __le__(self, other):
        return 0
    def  __gt__(self, other):
        return 0
    def __ge__(self, other):
        return 0
    
class Step(NoOpCompare):
    def __init__(self, l, idx):
        self.list = l
        self.idx = idx # next index to consider

class GraphStep(NoOpCompare):
    def __init__(self, g, idx):
        self.graph = g
        self.idx = idx # next index to consider