import socket
import re
import time
from datetime import datetime, timedelta
from urlparse import urlparse, parse_qs
import thread
from threading import Thread
from threading import Timer
import sys
port = 8016
host = "127.0.0.1"
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((host,port))
server_socket.listen(10)

sec_t_clock = int(time.strftime("%S"))
min_t_clock = int(time.strftime("%M"))
hour_t_clock = int(time.strftime("%H"))

def add_function(add,connection):
    value_time = datetime.now() + timedelta(seconds=add)
    print value_time , "to disconnet"
    while(True):
        print time.strftime("%M:%S")
        time.sleep(1)
        if value_time <= datetime.now():
            return connection.close()

def request_function(connection):
    print "Connection done:"
    received_data = connection.recv(1024)
    print received_data
    regex = 'GET (.+?) HTTP/1.1'
    pattern = re.compile(regex)
    result = re.findall(pattern,received_data)
    url = result[0]
    params = parse_qs(urlparse(url).query)
    connection.sendall("""<html><body><h1>This is your api</h1></body></html>\r\n""") # Use triple-quote string.
    # print int(params['timeout'][0])
    # add_function(int(params['timeout'][0]))
    add = int(params['timeout'][0])
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
        print "YES"
        #break
    except KeyboardInterrupt:
        break
    i=i+1
    print "OK"
