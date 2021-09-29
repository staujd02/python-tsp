
import array as arr
from source.dataStructures import Vector
from source.utilities.graphStringMuxer import GraphStringMuxer

from typing import List

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
    def demonstratesConsistency(register) -> bool:
        return register == arr.array('i', [1] * len(register))

    @staticmethod
    def __getDestinationIndex(vectorString: str) -> int:
        return GraphStringMuxer.translate(
                GraphStringMuxer.destintationCharacter(vectorString)
            )