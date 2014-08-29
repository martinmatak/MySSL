__author__ = 'k'
"""
http://www.binarytides.com/python-socket-programming-tutorial/
http://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate
"""
import socket
import ssl
import sys  # for exit
#import pprint


class MySSLClient(object):

    def __init__(self, cert_path, name, host, port):
        """
        :param host: host for connection
        :param port: port for connection
        :param name: the name of the instance.
        :param cert_path: the CA cert path in order to verify the identity of the other side.
        """
        self.name = name
        try:
            #create an AF_INET(IPV4), STREAM socket (TCP)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + str(msg[1])
            sys.exit()
        print self.name + 'Socket Created'
        self.host = host
        self.port = port
        try:
            socket.gethostbyname(self.host)
        except socket.gaierror:
            #could not resolve error
            print 'Hostname could not be resolved. Exiting'
            sys.exit()

        # Require a certificate from the server.
        # We used a self-signed certificate
        # so here ca_certs is the CA cert
        self.ssl_sock = ssl.wrap_socket(self.sock,
                                        ca_certs=cert_path,
                                        cert_reqs=ssl.CERT_REQUIRED)

    def connect_ssl(self):
        """
        connect to another server/client with ssl.
        """
        self.ssl_sock.connect((self.host, self.port))
        print self.name + "Connection Established"
        print self.name + "Connected to: " + repr(self.ssl_sock.getpeername())
        print self.name + "Encryption: " + str(self.ssl_sock.cipher())
        #print "[" + self.name + "] " + pprint.pformat(self.ssl_sock.getpeercert())

    def write_msg(self, msg):
        try:
            #Send the whole string
            self.ssl_sock.sendall(msg)
        except socket.error:
            #Send failed
            print 'Send failed'
            sys.exit()

    def read_msg(self):
        # Read a chunk of data.  Will not necessarily
        # read all the data returned by the server.
        data = self.ssl_sock.read(4096)  # read 4096 bytes.
        if data != "":
            print self.name + "received data from server:" + data

    def close(self):
        print self.name + "Closing"
        # note that closing the SSLSocket will also close the underlying socket
        self.ssl_sock.close()


Alice = MySSLClient("certificates\CA\ca.pem", "[Alice]", "localhost", 1337)
Alice.connect_ssl()
Alice.write_msg("text msg")
Alice.read_msg()
Alice.close()
#testing123