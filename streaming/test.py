import csv
import json
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
import queue
from multiprocessing import Process, Queue


def read_data():
    data = []
    with open('user_query.csv', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            data.append(row)
    return json.loads(json.dumps(data, indent=4))


data = read_data()
# work_queue = queue.Queue()
# q = Queue()
# for work in data:
#     work_queue.put(work)
#     q.put(work)
#     print(1)

print(1)

def callback(x):
    d = [x]
    for i in range(1000):
        a = 1 + 2
        d.append(a)
    return 1
print(2)

start = time.time()
with ProcessPoolExecutor(max_workers=None) as executor:
    results = executor.map(callback, data)
print(3)

print(results.__sizeof__())
print(time.time() - start)

# start = time.time()
# procs = []
# num_thread = multiprocessing.cpu_count()
# num_queries = len(data)
# query = [data[i * num_queries: (i + 1) * num_queries] for i in range(num_thread)]
#
# for qe in range(num_thread):
#     proc = Process(target=callback, args=(q,))
#     procs.append(proc)
#     proc.start()
# for proc in procs:
#     proc.join()
#
# print(results.__sizeof__())
# print(time.time() - start)
