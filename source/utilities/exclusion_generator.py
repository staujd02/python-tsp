from copy import deepcopy
from source.utilities.graham_scan import GrahamScan

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
   def generateExclusionDictionaryTrials(points):
       myList = deepcopy(points)
       exclusions = {}
       while(len(myList) > 3):
            hullList = GrahamScan.getConvexHull(myList)
            myList = list(filter(lambda x: x not in hullList, myList))
            if len(hullList) > 3:
                exclusions.update(ExclusionGenerator.generateExclusionDictionary(hullList))
       return exclusions

   @staticmethod
   def __getIdentifiers(hull):
       return list(map(lambda p: p[2], hull))