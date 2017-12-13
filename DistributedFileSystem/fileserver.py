import sys, SocketServer, threading, os, re
import Queue

from cache import Cache
from locker import Locker

DFS_ROOT_DIR = "~/DFS-FILES/"
initialized = False

class ThreadPoolMixIn(SocketServer.ThreadingMixIn):

    pool_size = 10 #No. of threads in the pool
    student_id = "07988616e4e32911bc9f6a7571184b611fc93406d027a5c828a87664735ed383"
    dir_current = DFS_ROOT_DIR
    cache = Cache()
    locker = Locker()
    initialized = False
    root_dir = None
    
    """
    =========================================================
                THREAD INITIALIZATION FUNCTIONS
    =========================================================
    """
    #Main server loop
    def serve_always(self):
        #Create the request queue
        self.request_queue = Queue.Queue(self.pool_size)
        for t in range(self.pool_size):
            t = threading.Thread(target = self.process_request_thread) #Initialize threads
            #print "Starting pool thread ", t.name
            t.start()

        while 1:
            self.handle_request() #Get the ball rolling

    #Start handling the requests sent to the server
    def handle_request(self):
        #requests are esentially socket objects
        request, client_address = self.get_request()
        #Place in the queue
        self.request_queue.put((request,client_address))

    #Get a request from the queue
    def process_request_thread(self):
        while 1:
            #ThreadingMixIn.process_request_thread(self, self.request_queue.get())
            try:
                request, client_address = self.request_queue.get()
            except Queue.Empty:
                pass
            #Fufill request
            self.finish_request(request, client_address)

    """========================================================="""

