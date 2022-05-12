from multiprocessing import Process
import time
pop=40


def func():
    print("starting")
    for i in range(1000):
      print(i)
    

if __name__ == "__main__":  # confirms that the code is under main function
    procs = []

    # instantiating process with arguments
    for i in range(pop):
        # print(name)
        proc = Process(target=func)
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()
