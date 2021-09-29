arrowString = '->'

class GraphStringMuxer(object):

    arrowString = '->'

    @staticmethod
    def translate(key):
        return ord(key) - 65
    
    @staticmethod
    def destintationCharacter(vectorString: str) -> str:
        return vectorString[1 + len(arrowString)]