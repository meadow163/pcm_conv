from multiprocessing import Process,Pool
import threading
import time
  
def foo(i):
    #print 'say hi',i
    #time.sleep(5)
    print 'say hi',i

pool = Pool(20)

for i in range(10):
    p = Process(target=foo,args=(i,))
    p.start() 
    #p.join()


print('assian end,main pro end')
