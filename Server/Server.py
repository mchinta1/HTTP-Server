import socket
import  os
import threading
import time
from email.utils import formatdate
import mimetypes
import random



class MyServer(threading.Thread):
    def __init__(self,client_connection,ip,port):
        threading.Thread.__init__(self)
        self.client_connection = client_connection
        self.ip = ip
        self.port = port

    def run(self):



        request = self.client_connection.recv(1024).decode('utf-8')
       # print(request)

        string_list = request.split(" ")
        method = string_list[0]
        resource = string_list[1]
        resource = resource[1:]




        #print(p)
        file_path = p + resource
        try:
            print("file:",file_path)
            f = open(file_path, 'rb')
            l = f.read()
            with my_lock:
                my_dict[resource] += 1
            f.close()

            print("Client {0} connected on port {1} requested for {2} count - {3}".format(self.ip, self.port,resource,my_dict[resource]))

            date = formatdate(timeval=None, localtime=False, usegmt=True)

            type = mimetypes.guess_type(file_path,True)
           # print(type[0])
            m=os.path.getmtime(file_path)
            m= formatdate(timeval=m,localtime=False,usegmt=True)
            r = "HTTP/1.1 200 OK\r\n"+"Content-Length: " + str(len(l))+ "\r\n" + "Content-Type: "+ type[0] +"; charset=utf-8\r\n"+"Date: "+date+"\r\n" + "Server: Mani v1.1\r\n"+"Last-Modified: "+m+"\r\n" + "\r\n";
           # print(r)
            r = r.encode("utf-8")
            self.client_connection.send(r+l);
           # print(r)
           # print(r.decode('utf-8'))
        except BaseException as e:
            print(e)
            header = 'HTTP/1.1 404 FILE NOT FOUND\n'
            type = 'text/html'
            header += 'Content-Type:' + type
            final_response = header.encode('utf-8')
            self.client_connection.send(final_response)
        self.client_connection.close()
script_loc = os.path.abspath(__file__)
script_dir = os.path.split(script_loc)[0]
p = os.path.split(script_dir)[0]
p += "/www/"
print(p)
HOST = ''
PORT = random.choice(range(1024,49150,100))

g = os.listdir(p)

print("Files List: {0}".format(g))
my_dict = {}
for v in g:
    my_dict[v] = 0

print(my_dict)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listen_socket.bind((HOST, PORT))
threads = []

print ('Serving HTTP on port {0} ...'.format(PORT))
my_lock = threading.Lock()
while True:
    listen_socket.listen(5)
   # print(time.time())
    (client_connection, (ip,port) )= listen_socket.accept()
    t = MyServer(client_connection,ip,port)
    t.start()
    threads.append(t)

for t in threads:
    t.join()





