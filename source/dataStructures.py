
class Vector(object):

    start = ''
    end = ''
    length = 0

    def __init__(self, arg1, arg2=None, arg3=None):
        if arg2 == None or arg3 == None:
            self.__cloneVector(arg1)
        else:
            self.__createNewVector(arg1, arg2, arg3)

    def __cloneVector(self, vector):
        self.__createNewVector(vector.start, vector.end, vector.length)

    def __createNewVector(self, start, end, length):
       self.start = start 
       self.end = end
       self.length = length

    def isEqual(self, vector):
        return vector.start == self.start and vector.end == self.end and vector.length == vector.length

class ScanEntry(object):

    def __init__(self, arg1, arg2=None):
        if arg2 == None:
            self.__extractEntryFromList(arg1)
        else:
            self.__mapArgumentsToMembers(arg1, arg2)

    def __extractEntryFromList(self, list):
        self.name = list[0]
        self.path = list[1]

    def __mapArgumentsToMembers(self, name, path):
       self.name = name 
       self.path = path

    def toList(self):
        return [self.name, self.path]
    
    def getName(self):
        return self.name
    
    def getPath(self):
        return self.path
    
    def setName(self, name):
        self.name = name
    
    def setPath(self, path):
        self.path = path