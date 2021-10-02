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
                exclusionList = exclusionList + list(map(lambda uuid: [val, uuid], guidList[idx+2:]))
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
   def generateExclusionDictionaryDeepCut(points):
       myList = deepcopy(points)
       exclusions = {}
       listOfHullsLists = []
       while(len(myList) > 2):
            hullList = GrahamScan.getConvexHull(myList)
            myList = list(filter(lambda x: x not in hullList, myList))
            listOfHullsLists.append(deepcopy(hullList))
            if len(hullList) > 3:
                exclusions.update(ExclusionGenerator.generateExclusionDictionary(hullList))
       for [idx, hullList] in enumerate(listOfHullsLists):
           if idx == len(listOfHullsLists) - 1:
               break
           for pt in hullList:
               for interiorHull in listOfHullsLists[idx+1:]:
                    deepCut = GrahamScan.getConvexHull([pt] + interiorHull)
                    if len(deepCut) > 3:
                        # doing below would cross cut the deep cut - not sure if that's right?
                        # exclusions.update(ExclusionGenerator.generateExclusionDictionary(deepCut))
                        exclusionDictonary = {}
                        guidList = ExclusionGenerator.__getIdentifiers(deepCut)
                        exclusionDictonary[pt[2]] = guidList[idx+2:-1]
                        exclusionList = list(map(lambda uuid: [pt[2], uuid], guidList[idx+2:-1]))
                        for (idx, uuidPair) in enumerate(exclusionList):
                            if uuidPair[1] in exclusionDictonary:
                                exclusionDictonary[uuidPair[1]].append(uuidPair[0])
                            else:
                                exclusionDictonary[uuidPair[1]] = [uuidPair[0]]
                        for idx, (key, destinationList) in enumerate(exclusionDictonary.items()):
                            if key not in exclusions:
                                exclusions[key] = destinationList
                            else:
                                for val in destinationList:
                                    if val not in exclusions[key]:
                                        exclusions[key].append(val)
       return exclusions
   
   @staticmethod
   def generateExclusionDictionaryDeepWebCut(points):
       myList = deepcopy(points)
       exclusions = {}
       listOfHullsLists = []
       while(len(myList) > 2):
            hullList = GrahamScan.getConvexHull(myList)
            myList = list(filter(lambda x: x not in hullList, myList))
            listOfHullsLists.append(deepcopy(hullList))
            if len(hullList) > 3:
                exclusions.update(ExclusionGenerator.generateExclusionDictionary(hullList))
       for [idx, hullList] in enumerate(listOfHullsLists):
           if idx == len(listOfHullsLists) - 1:
               break
           for pt in hullList:
               for interiorHull in listOfHullsLists[idx+1:]:
                    deepCut = GrahamScan.getConvexHull([pt] + interiorHull)
                    if len(deepCut) > 3:
                        exclusionDictonary = ExclusionGenerator.generateExclusionDictionary(deepCut)
                        for idx, (key, destinationList) in enumerate(exclusionDictonary.items()):
                            if key not in exclusions:
                                exclusions[key] = destinationList
                            else:
                                for val in destinationList:
                                    if val not in exclusions[key]:
                                        exclusions[key].append(val)
       return exclusions

   @staticmethod
   def __getIdentifiers(hull):
       return list(map(lambda p: p[2], hull))