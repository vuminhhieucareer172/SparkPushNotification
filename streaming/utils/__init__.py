import time
from multiprocessing import Process


def print_func(continent='Asia'):
    time.sleep(0.1)
    print('The name of continent is : ', continent)


if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa']
    procs = []
    proc = Process(target=print_func)  # instantiating without any argument
    procs.append(proc)
    start = time.time()
    proc.start()

    # instantiating process with arguments
    for name in names:
        # print(name)
        proc = Process(target=print_func, args=(name,))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()
    print(time.time() - start)

    start2 = time.time()
    print_func()
    for name in names:
        print_func(name)
    print(time.time() - start2)
