
class ExclusionGenerator(object):

   @staticmethod
   def generateExclusionList(hullList):
        exclusionList = []
        guidList = ExclusionGenerator.__getIdentifiers(hullList)
        for (idx, val) in enumerate(guidList):
            if idx == 0:
                exclusionList = exclusionList + list(map(lambda uuid: [val, uuid], guidList[idx+2:-1]))
            elif idx < len(guidList) - 2:
                exclusionList = exclusionList + list(map(lambda uuid: [val, uuid], guidList[idx+2:]))
            else:
                break
        return exclusionList + list(map(lambda uuidPair: [uuidPair[1], uuidPair[0]],exclusionList))

   @staticmethod
   def __getIdentifiers(hull):
       return list(map(lambda p: p[2], hull))