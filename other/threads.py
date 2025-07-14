import threading

counter = 0

def incresse_global_counter():
    global counter
    for _ in range(100000):
        counter += 1
        print(counter)

def decress_global_counter():
    global counter
    for _ in range(100000):
        counter -= 1
        print(counter)


thread1 =  threading.Thread(target=incresse_global_counter)
thread2 =  threading.Thread(target=decress_global_counter)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("final counter value:", counter)