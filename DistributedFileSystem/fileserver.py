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

 def find_file(self, path):
        return os.path.exists(path)


    def read_file(self, path):
        #If the file is in the cache, retreive from there
        if self.cache.search(path):
            data = self.cache.retrieve(path)
            print "{0} retrieved from cache".format(path)
            return data
        else:
        #Retreive data the standard way
            if '/' in path:
                full_dir = os.path.expanduser(path)

                if not self.find_file(full_dir):
                    return "No such file or directory"

                #File is found, change the directory
                path1, file = os.path.split(full_dir)
                try:
                    os.chdir(path1)
                except OSError:
                    #The other one should've caught this
                    return "No such file or directory"
            else:
                #File is in the current directory
                file = path
            #Try to acquire the lock
            if not self.locker.acquire_lock(file):
                locked = "File is locked, no cached copy available"
                return locked
            else:
                try:
                    fo = open(file, "r")
                except IOError:
                    return "No such file or directory - open"
                data = fo.read()
                fo.close()
                #Release the lock
                self.locker.release_lock(file)
                self.cache.add(path, data)
                return data

    def write_file(self, data_in):
        #Seperate out the two components
        path = data_in[0]
        data =  data_in[1]
        if '/' in path:
            #User entered path in the form ~/DFS-FILES/path
            if "~/DFS-FILES" in path:
                full_dir = os.path.expanduser(path)
            else:
                #User implied the working dir; append it to the path
                full_dir = os.getcwd() + '/' + path

            path1, file = os.path.split(full_dir)
            try:
                os.chdir(path1)
            except OSError:
                #If the dir does not exist - make it
                print "Directory does not exist; creating..."
                os.mkdir(path1)
                os.chdir(path1)
        else:
            file = path
        #Try to acquire the lock
        if not self.locker.acquire_lock(file):
            locked = "File is locked, no cached copy available"
            return locked
        else:
            fo = open(file, "w")
            fo.write(data)
            fo.close()
            #Release the lock
            self.locker.release_lock(file)
            response = "File {0} has been written\n".format(path)
            return response

    """========================================================="""
