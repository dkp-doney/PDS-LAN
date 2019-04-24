import socket
#from MasterThread import MasterThread
#from SplitDownloader import * 
import select
#import merge
from threading import Thread
#import socket
import os
#import select
#import seekmer
#import socket
#from MasterThread import MasterThread
#from SplitDownloader import * 
#import select
#import merge
import urllib.request
import urllib.response
#import os
#import seekmer
#import os.path
import sys
import shutil
import time










class recive_tcp_message:
        def __init__(self,):
            self.BUFFER_SIZE = 1024
            self.list_of_param = []
            self.threads = []
            self.sequence = 0
        def tcp_listen(self,tcpsock):
            read_list = [tcpsock]
            tcpsock.listen(1)
            print ("Waiting for incoming connections...")
            #while True:
            try:
                readable, writable, errored = select.select(read_list, [], [],1)
                for s in readable:
                    if s is tcpsock:
                        (conn, (ip,port)) = tcpsock.accept()
                        msg=conn.recv(self.BUFFER_SIZE)
                        self.sequence = self.sequence+1
                        print(msg,self.sequence)
                        
                        print("Got connection from client ",self.sequence, (ip,port))
                        self.list_of_param.append([ip,port,conn,self.sequence])
                        

                    else:
                        pass
                            
            except socket.timeout:
                    pass
        def tcp_thread(self):    
            for i in self.list_of_param:
                print(i)
            #code to pass url here
            #@TODO get url from user
            #url='https://www.w3.org/TR/PNG/iso_8859-1.txt'
            url='https://www.codesector.com/files/teracopy.exe'
            client_url=Start_split(url,self.sequence)
            #starting threads
            for i in range(self.sequence) :
                newthread = MasterThread(self.list_of_param[i],client_url[i])
                newthread.start()
                self.threads.append(newthread)
            #for t in self.threads:
                

            for t in self.threads:
                t.join()
            merge(url,self.sequence)






def broadcast_send():
        rtm=recive_tcp_message()
        tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpsock.bind(('', 9001))
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        server.settimeout(0.02)
        server.bind(("", 44444))
        message = b"broadcast from server"
        timeout = 30   # [seconds]
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            server.sendto(message, ('<broadcast>', 37020))
            print("brodcast message sent!")
            time.sleep(1)
            rtm.tcp_listen(tcpsock)
        if rtm.sequence != 0 :
            rtm.tcp_thread()
        else :
            print("Search failed no client devices found")
            





class MasterThread(Thread):
    

    def __init__(self,param,url): #recives a tuple param from listofparam and a list clientlist
        Thread.__init__(self)
        self.ip = param[0]
        self.port = param[1]
        self.sock = param[2]
        self.sequence = param[3]
        self.url = url[0]
        self.byte = url[1]
        print(" New thread started for client-"+str(self.sequence)+"  :"+self.ip+":"+str(self.port))
      
    def run(self):
         read_list = [self.sock]   
         #print("hello")
         msg="Client-"+str(self.sequence)
         
        # print(type(self.sock))
         #self.sock.send(msg.encode())
         ##print(msg)
         ##print(self.url)
         #self.sock.send(self.url.encode())
         #print(self.byte)
         self.sock.send(self.byte.encode())
         print("download link send to"+str(self.sequence))
         def recvall(sock):
            BUFF_SIZE = 4096 # 4 KiB
            data = b''
            while True:
                part = sock.recv(BUFF_SIZE)
                #p1=part.decode()
                data += part
                #if len(part) < BUFF_SIZE:
                if not part:
                    # either 0 or end of data
                    break
            return data
         readable, writable, errored = select.select(read_list, [], [])   
         for s in readable:
             if s is self.sock:



                #while True:   
                part=recvall(self.sock)
                #find offset
                #bt = str(self.byte)
                #temp=(bt.split('='))
                #temp1=(temp[1].split('-'))
                #temp2=temp1[0]
                #offset=int(temp2)

                #print("startng pos to write data:",offset)
                #seekmer.replace(offset,part)
                

                    #print(part)
                downloadFolder = "C://Project/parellel-download"
                if not (os.path.isdir("C://Project/parellel-download")):
                    os.makedirs("C://Project/parellel-download")
                downloadpath = downloadFolder + "/" + "new_file"   
                f=open(downloadpath+str(self.sequence),"wb")
                print("data from client",self.sequence,"is received")
                f.write(part)
                print("data from client",self.sequence,"is written to file")
                f.close()
                #print(part)







class HeadRequest(urllib.request.Request):
    def get_method(self):
        return "HEAD"
def n_division(client_count,contentlength):
    lis=[]
    segmentSize=int(contentlength/client_count)
    top=segmentSize
    s='bytes=0-'+str(segmentSize)
    lis.append(s)
    for i in range(client_count-1):
        newTop=top+segmentSize
        s='bytes='+str(top+1)+"-"+str(newTop)
        lis.append(s)
        top=newTop
    return lis
def Start_split(url,client_count):
        url = url
        client_count = client_count
        writepath = 'file.txt'
        mode = 'ab' if os.path.exists(writepath) else 'wb+'
        req = HeadRequest(url)
        response = urllib.request.urlopen(req)
        response.close()
        print("Fileinfo ==>")
        print(response.info())
        strRes = str(response.info())
        contentlength=int(response.getheader("Content-Length"))
        
        print(" N-Division requests")
        print("\tNo. of clients:",client_count)
        print("\tFileSize in bytes:",contentlength)
        #seekmer.create(contentlength)
        #print("sample file of content length created")
        urlRangeList = n_division(client_count,contentlength)
        for a in urlRangeList:
            print(a)
        requests = []
        for x in urlRangeList:
            ss = "urllib.request.Request(" + url + ", headers={'Range':" + x + "})"
            requests.append(ss)
        # pass urlRangeList[i] to the clients_list[i]
        for i in range(client_count):
            clients = [[url,xx] for xx in urlRangeList]

        for test in clients:
            print (test)


        print("done")
        return clients





def merge(url,seq):
    i=1
    buffer_size=8192
    downloadname =str(url.split('/')[-1])#gives proper filename
    downloadFolder = "c://project/parellel-download"
    downloadPath = downloadFolder + "/" + "new_file"
    fdst=open(downloadFolder+"/"+downloadname,"wb")
    while(i<=seq):
        if (os.path.isfile(downloadPath+str(i))): 
            fsrc=open(downloadPath+str(i),"rb")
            print("merging...file from client",i)
            shutil.copyfileobj(fsrc,fdst,buffer_size)
            #dt=g.read()
            #fn.write(dt)
            print("client ",i,"file merged")

            i=i+1
        else:
            print("file from client",i,"is missing program is exiting..." )
            sys.exit(0)
            break
    #fsrc.close()
    fdst.close()
    print("Hurray!!!  completed succesfully....")




broadcast_send()