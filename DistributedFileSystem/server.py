#!/bin/bash
import sys, socket, SocketServer, threading, os, re
import Queue

from cache import Cache
from locker import Locker
from fileserver import FileServer

DFS_ROOT_DIR = "~/DFS-FILES/"
FILE_SERVER1_DIR = "~/DFS-FILES/"
FILE_SERVER2_DIR = "~/DFS-FILES/test/"


class ThreadPoolMixIn(SocketServer.ThreadingMixIn):

    pool_size = 10 #No. of threads in the pool
    student_id = "07988616e4e32911bc9f6a7571184b611fc93406d027a5c828a87664735ed383"
    dir_current = DFS_ROOT_DIR
    cache = Cache()
    locker = Locker()
    servers = {}
     
    #fs1 = FileServer(("0.0.0.0", 2049), ThreadedRequestHandler)
    #fs2 = FileServer(("0.0.0.0", 2050), ThreadedRequestHandler)
    
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Connect to first file server and pass its directory
    address1 = ("0.0.0.0", 2049)
    s1.connect(address1)
    s1.send(FILE_SERVER1_DIR)
    data = s1.recv(512)
    print data
    servers[FILE_SERVER1_DIR] = s1 
    
    #Connect to second file server and pass its directory
    address2 = ("0.0.0.0", 2050)
    s2.connect(address2)
    s2.send(FILE_SERVER2_DIR)
    data = s2.recv(512)
    print data
    servers[FILE_SERVER2_DIR] = s2 
    
    socketToSend = s1
    
    """
    =========================================================
                THREAD INITIALIZATION FUNCTIONS
    =========================================================

"""
    =========================================================
                    DIRECTORY OPERATIONS
    =========================================================
    """

    def dir_change(self, path):
        #if path == os.pardir:
        if path == "..":
            self.dir_current = os.path.dirname(os.path.normpath(self.dir_current))
        elif os.path.exists(path):
            self.dir_current += path

        if not self.dir_current.endswith('/'):
                self.dir_current += '/'
        else:
            return -1
        
        self.resolve_socket(self.dir_current)
        return self.dir_current

    def dir_list(self, path):
        path = os.path.expanduser(path)
        lst = os.listdir(path)
        dirlst = ""
        for i in lst:
            dirlst += i + '\n'

        return dirlst

    """========================================================="""

    """
    =========================================================
                    THREAD MAIN LOOP
    =========================================================
    """

    #This is where the work is done
    def finish_request(self, request, client_address):
        while 1:
            #Recieve data from client
            data = request.recv(8192)
            root_dir = os.path.expanduser(DFS_ROOT_DIR)
            os.chdir(root_dir)

            """
            N/B: Requests will of the form <COMMAND> <DIR> <DATA>
            e.g. READ_FILE ~/DFS-FILES/loremipsum.txt
            <COMMANDS> :  READ FILE <DIR>
                          WRITE FILE <DIR> <DATA>
                          CHDIR <DIR>
                          PWDIR <DIR>
                          LS
            """
            if not data:
                response = "The directory server received nothing"
                request.sendto(response, client_address)
            else:
                if data.startswith("READ FILE"):
                    r = re.compile("READ FILE (.*?)$")
                    res = r.search(data)
                    path = res.group(1)
                    self.socketToSend.send(data)
                    response = self.socketToSend.recv(8192)
                    #response = self.read_file(path)
                    request.sendto(response, client_address)

                if data.startswith("WRITE FILE"):
                    #r = re.compile("WRITE FILE (.*?)$")
                    #res = r.search(data)
                    #s = res.group(1)
                    #data = s.split(" ", 1)
                    self.socketToSend.send(data)
                    response = self.socketToSend.recv(8192)
                    #response = self.write_file(data)
                    request.sendto(response, client_address)

                if data.startswith("PWD"):
                    response = self.dir_current
                    request.sendto(response, client_address)

                if data.startswith("CD"):
                    r = re.compile("CD (.*?)$")
                    res = r.search(data)
                    path = res.group(1)
                    if self.dir_change(path) == -1:
                        response = "Path or directory does not exist"
                        request.sendto(response, client_address)
                    else:
                        #Have to send something, as the client expects a response
                        request.sendto(" ", client_address)

                if data.startswith("LS"):
                    response = self.dir_list(self.dir_current)
                    request.sendto(response, client_address)


                if data.startswith("QUIT"):
                    for key in self.servers:
                        sock = self.servers[key]
                        sock.send(data)
                        
                    print "Shutting down Directory Server"
                    self.shutdown()


    """========================================================="""
