import random
import threading

class MyThread(threading.Thread):
    def __init__(self, ID, name, jobs, uniques):
        threading.Thread.__init__(self)
        self.ID = ID
        self.name = name
        self.jobs = jobs
        self.uniques = uniques
        self.lock = threading.Lock()
        self.countUniques = 0

    def run(self): # override the default run() method, job for each thread
        #print("Thread " + str(self.ID) + " starting")

        while (True):            
            #lock other threads
            self.lock.acquire() #<----starting critical section ------ 
            print("\tThread " + str(self.ID) + " is running")
            if len(self.jobs) == 0:
                break
            #pull a number from queue
            temp = self.jobs.pop()
            if temp not in self.jobs:
                print("New unique value: " + str(temp))
                self.countUniques += 1  
            self.lock.release() #<----end of critical section ------

def main():
    countUniques = 0

    # 1. (20pts) Insert 20 random integers in the range [10, 30] into a queue named jobs. Print those random integers on the screen.
    jobs = jobsQueue(20, 10, 30)
    print("Question 1: \n\t" + str(jobs))
    print("\tExpected Length: " + str(len(set(jobs))))

    # 2. (20pts) In main(), create 5 threads, each having a unique ID (e.g., thread 1â€™s ID is 1, thread 2â€™s ID is 2, and so on). 
    thread1 = MyThread(1, "1", jobs, countUniques)
    print("Question 2: \n\tThread: " + str(thread1.ID))
    thread2 = MyThread(2, "2", jobs, countUniques)
    print("\tThread: " + str(thread2.ID))
    thread3 = MyThread(3, "3", jobs, countUniques)
    print("\tThread: " + str(thread3.ID))
    thread4 = MyThread(4, "4", jobs, countUniques)
    print("\tThread: " + str(thread4.ID))
    thread5 = MyThread(5, "5", jobs, countUniques)
    print("\tThread: " + str(thread5.ID))

    # 3. (20pts) Each thread gets an integer from the queue jobs. If this integer is unique, this thread prints the integer on the screen, and increases countUniques by 1 (countUniquesâ€™s initial value is 0).
    print("Question 3: ")
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()

    # 4. (20pts) In main(), after all threads finish work, print countUniquesâ€™s value on the screen. [If jobs has 20 random integers but there are 15 unique ones, then we should see 15 on the screen.] 
    countuniques = thread1.countUniques + thread2.countUniques + thread3.countUniques + thread4.countUniques + thread5.countUniques
    print("Question 4: \n\t Uniques: " + str(countuniques))

def jobsQueue(count, min, max):
    jobs = []
    for x in range(0,20):
        jobs.append(random.randint(10, 30)) 
    return jobs

if __name__== '__main__':
    main()

