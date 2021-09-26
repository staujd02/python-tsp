
class ExclusionGenerator(object):
   
   @staticmethod
   def generateExclusionDictionary(hullList):
        exclusionDictonary = {}
        exclusionList = []
        guidList = ExclusionGenerator.__getIdentifiers(hullList)
        for (idx, val) in enumerate(guidList):
            if idx == 0:
                exclusionDictonary[val] = guidList[idx+2:-1]
                exclusionList = exclusionList + list(map(lambda uuid: [val, uuid], guidList[idx+2:-1]))
            elif idx < len(guidList) - 2:
                exclusionDictonary[val] = guidList[idx+2:]
                exclusionList =  exclusionList + list(map(lambda uuid: [val, uuid], guidList[idx+2:]))
            else:
                exclusionDictonary[val] = []
        for (idx, uuidPair) in enumerate(exclusionList):
            exclusionDictonary[uuidPair[1]].append(uuidPair[0])
        return exclusionDictonary

   @staticmethod
   def __getIdentifiers(hull):
       return list(map(lambda p: p[2], hull))