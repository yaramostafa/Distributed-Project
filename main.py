import threading
import ChatClient as CC
import CarClient as Car

#t2 = threading.Thread(target=Car.startCar)
t1 = threading.Thread(target=CC.initChat, args=('Hello', ))
t1.start()
#t2.start()