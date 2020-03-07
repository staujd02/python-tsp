import time

class Timer(object):

    @staticmethod
    def time(message, thingToDo, returnTup=False):
        start = time.time()
        x = thingToDo()
        end = time.time()
        runTime = end - start
        print(message + str(runTime))
        if returnTup:
            return (x, runTime)
        return x