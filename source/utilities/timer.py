import time


class Timer(object):

    @staticmethod
    def time_execution(message, thing_to_do):
        start = time.time()
        x = thing_to_do()
        end = time.time()
        runTime = end - start
        print(message + str(runTime))
        return x

    @staticmethod
    def get_timed_result(message, thingToDo):
        start = time.time()
        x = thingToDo()
        end = time.time()
        runTime = end - start
        print(message + str(runTime))
        return (x, runTime)
