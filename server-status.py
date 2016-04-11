import socket
import re
import time
from datetime import datetime, timedelta
from urlparse import urlparse, parse_qs
import thread
from threading import Thread
from threading import Timer
import threading
import sys
port = 8022
host = "127.0.0.1"
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((host,port))
server_socket.listen(10)

def add_function(add,connection):
    value_time = datetime.now() + timedelta(seconds=add)
    print value_time , "to disconnect"
    while(True):
        #print time.strftime("%M:%S")
        time.sleep(1)
        if value_time <= datetime.now():
            connection.send('{"status":"ok"}')
            return connection.close()

#def thread_list():
#    int(params['connId'][0])
active_threads = {}
active_Id = []
def Alive_threads():
    total_threads = len(threadlist)
    #print total_threads
    i=0
    #while(i<total_threads):
    for t in threadlist:
        #if(threadlist[i].isAlive):
        if(t.isAlive()):
            #active_threads[i+1] = active_Id[i]
            #print i
            active_threads.update({i+1:active_Id[i]})
        i=i+1
    return active_threads
    #length_active = len(active_threads)
    #new_active_threads = {}
    # for j in range(0,length_active):
    #     if(active_threads[j]==-1):
    #         continue
    #     else:
    #         new_active_threads.update({j+1:active_threads[j]})

def request_function(connection):
    print "Connection done:"
    received_data = connection.recv(1024)
    print received_data
    regex = 'GET (.+?) HTTP/1.1'
    pattern = re.compile(regex)
    result = re.findall(pattern,received_data)
    url = result[0]
    params = parse_qs(urlparse(url).query)
    #print result
    if(result[0]=='/api/serverStatus'):
        active_Id.append(-1)
        #print threadlist
        #print active_Id
        active_values = str(Alive_threads())
        connection.send(active_values)
        connection.close()


        # for i in range(0,threadlist):
        #     #check whether a thread is active of not
        #     #if thread is active
        #     array_active[i+1] = id_thread

    else:
        connection.send("""<html><body><h1>This is your api</h1></body></html>\r\n""") # Use triple-quote string.
        # print int(params['timeout'][0])
        # add_function(int(params['timeout'][0]))
        add = int(params['timeout'][0])
        connId = params['connId'][0]
        #threadlist.append(connId)
        active_Id.append(connId)
        #print threadlist
        #print active_Id
        return add_function(add,connection)
        # threadlist_new = []
        # t = Thread(target=add_function,args=(add,connection,))
        # t.start()
        # threadlist_new.append(t)
        # return request_function(connection)

i=1
threadlist = []
while(True):
    connection , Cli_Addr = server_socket.accept()
    #request_function(connection)
    print i , "Connection number"
#while(True):
    try:
        t = Thread(target=request_function,args=(connection,))
        t.start()
        threadlist.append(t)
        #print "YES"
        #break
    except KeyboardInterrupt:
        break
    i=i+1
    #print "OK"
