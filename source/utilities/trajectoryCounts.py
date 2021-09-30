
import array as arr
from source.dataStructures import Vector
from source.utilities.graphStringMuxer import GraphStringMuxer

from typing import List, Union

class TrajectoryCounts(object):

    @staticmethod
    def fillRegister(graphData: List[str]) -> str:
        register = arr.array('i', [0] * len(graphData))
        for v in graphData:
            destinationIndex = TrajectoryCounts.__getDestinationIndex(v)
            register[destinationIndex] += 1
        return register
    
    @staticmethod
    def createDeltaRegister(register, vectorStringRemoving: str, newVector: Vector):
        newRegister = arr.array('i', register)
        oldDestinationIndex = TrajectoryCounts.__getDestinationIndex(vectorStringRemoving)
        newRegister[oldDestinationIndex] -= 1
        newDestinationIndex = GraphStringMuxer.translate(newVector[1]) 
        newRegister[newDestinationIndex] += 1
        return newRegister
    
    @staticmethod
    def demonstratesConsistency(register, startIndex = 0) -> Union[bool, int]:
        for idx in range(startIndex, len(register)):
            if register[idx] != 1:
                return [False, idx]
        for idx in range(0, len(register) - (len(register) - startIndex)):
            if register[idx] != 1:
                return [False, idx]
        return [True, startIndex]

    @staticmethod
    def __getDestinationIndex(vectorString: str) -> int:
        return GraphStringMuxer.translate(
                GraphStringMuxer.destintationCharacter(vectorString)
            )