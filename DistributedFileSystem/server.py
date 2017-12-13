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
    