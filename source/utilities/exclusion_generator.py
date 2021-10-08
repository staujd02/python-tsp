from copy import deepcopy
from source.utilities.graham_scan import GrahamScan

class ExclusionGenerator(object):
   
   @staticmethod
   def generateExclusionsByHullRings(points):
       [exclusions, _] = ExclusionGenerator.createHullRings(deepcopy(points), 3)
       return exclusions
   
   @staticmethod
   def generateExclusionsWithDeepCutsAroundHullRings(points):
       [exclusions, listOfHullsLists] = ExclusionGenerator.createHullRings(deepcopy(points), 2)
       for [idx, hullList] in enumerate(listOfHullsLists):
           if idx == len(listOfHullsLists) - 1:
               break
           for pt in hullList:
               for interiorHull in listOfHullsLists[idx+1:]:
                    deepCut = GrahamScan.getConvexHull([pt] + interiorHull)
                    if len(deepCut) > 3:
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
       [exclusions, listOfHullsLists] = ExclusionGenerator.createHullRings(deepcopy(points), 2)
       for [idx, hullList] in enumerate(listOfHullsLists):
           if idx == len(listOfHullsLists) - 1:
               break
           for pt in hullList:
               for interiorHull in listOfHullsLists[idx+1:]:
                    ExclusionGenerator.runExclusionsOnPointList(exclusions, [pt] + interiorHull)
       return exclusions
   
   @staticmethod
   def generateExclusionDictionaryDeepWebCutWithWindows(points):
       [exclusions, listOfHullsLists] = ExclusionGenerator.createHullRings(deepcopy(points), 2)
       for [hdx, hullList] in enumerate(listOfHullsLists):
           if hdx == len(listOfHullsLists) - 1:
               break
           for [idx, pt] in enumerate(hullList):
               for interiorHullList in listOfHullsLists[hdx+1:]:
                    interiorHull = deepcopy(interiorHullList)
                    ExclusionGenerator.runExclusionsOnPointList(exclusions, [pt] + interiorHull)
                    [left, right] = ExclusionGenerator.getLeftRightOfIdx(hullList, idx) 
                    ExclusionGenerator.runExclusionsOnPointList(exclusions, [pt, right]  + interiorHull)
                    ExclusionGenerator.runExclusionsOnPointList(exclusions, [pt, left]  + interiorHull)
                    ExclusionGenerator.runExclusionsOnPointList(exclusions, [pt, left, right]  + interiorHull)
       return exclusions
   
   @staticmethod
   def getRight(hullList, idx):
       if idx == len(hullList) - 1:
            return hullList[0]
       return hullList[idx + 1]

   @staticmethod
   def getLeftRightOfIdx(hullList, idx):
       if idx == 0:
            return [hullList[len(hullList) - 1], hullList[idx + 1]]
       if idx == len(hullList) - 1:
            return [hullList[idx - 1], hullList[0]]
       return [hullList[idx - 1], hullList[idx + 1]]

   @staticmethod
   def runExclusionsOnPointList(exclusions, points):
       deepCut = GrahamScan.getConvexHull(points)
       if len(deepCut) > 3:
           exclusionDictonary = ExclusionGenerator.generateExclusionDictionary(deepCut)
           for idx, (key, destinationList) in enumerate(exclusionDictonary.items()):
               if key not in exclusions:
                   exclusions[key] = destinationList
               else:
                   for val in destinationList:
                       if val not in exclusions[key]:
                           exclusions[key].append(val)

   @staticmethod
   def createHullRings(pointList, threshold):
       exclusions = {}
       listOfHullsLists = []
       while(len(pointList) > threshold):
            hullList = GrahamScan.getConvexHull(pointList)
            pointList = list(filter(lambda x: x not in hullList, pointList))
            listOfHullsLists.append(deepcopy(hullList))
            if len(hullList) > 3:
                exclusions.update(ExclusionGenerator.generateExclusionDictionary(hullList))
       return [exclusions, listOfHullsLists]
   
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
   def __getIdentifiers(hull):
       return list(map(lambda p: p[2], hull))