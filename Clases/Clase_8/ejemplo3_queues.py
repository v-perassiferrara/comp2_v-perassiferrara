from multiprocessing import Queue

q = Queue()
q.put("dato")
print(q.get())