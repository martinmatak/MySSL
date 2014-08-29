__author__ = 'k'

import socket
import ssl
import sys  # for exit
#import pprint

HOST = ''  # Symbolic name meaning all available interfaces
PORT = 1337  # Arbitrary non-privileged port


class MySSLServer(object):

    def __init__(self,  name):
        self.name = name
        self.bind = None
        self.ssl_sock = None
        self.sock = None

    def start_server(self):
        """
        inits a new MySSL server object with HOST & PORT.
        """
        #create an AF_INET(IPV4), STREAM socket (TCP)
        self.bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.bind.bind((HOST, PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        self.bind.listen(10)
        print self.name + 'Socket now listening'

    def recv_ssl_data(self):
        while True:
            self.sock, addr = self.bind.accept()
            self.ssl_sock = ssl.wrap_socket(self.sock,
                                            server_side=True,
                                            certfile="certificates\server\server.pem",
                                            keyfile='certificates\server\server.key')
            print self.name + 'Connected with ' + addr[0] + ':' + str(addr[1])
            try:
                data = self.ssl_sock.recv(4096)
                print self.name + "received data from client: " + data
                reply = 'OK...'
                if not data:
                    break
                self.ssl_sock.sendall(reply)
            finally:
                self.ssl_sock.shutdown(socket.SHUT_RDWR)
                self.ssl_sock.close()


Bob = MySSLServer("[Bob]")
Bob.start_server()
Bob.recv_ssl_data()