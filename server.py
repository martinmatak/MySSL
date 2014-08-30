__author__ = 'k'

import hashlib
import socket
import ssl
import sys  # for exit
import json
import binascii  # ascii to binary
from Crypto.Cipher import AES


HOST = ''  # Symbolic name meaning all available interfaces
PORT = 1337  # Arbitrary non-privileged port

#TODO: add threads to server.
#TODO: give better names to functions

class MySSLServer(object):
    def __init__(self, name):
        self.name = name
        self.bind = None
        self.ssl_sock = None
        self.sock = None
        self.master = None

    def start_server(self):
        """
        inits a new MySSL server object with HOST & PORT.
        """
        # create an AF_INET(IPV4), STREAM socket (TCP)
        self.bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.bind.bind((HOST, PORT))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        self.bind.listen(1)
        print '%s Socket now listening' % self.name

    def myssl_cert_server(self):
        """
        This function does the following
        with public key encryption
        """
        while True:
            self.sock, addr = self.bind.accept()
            self.ssl_sock = ssl.wrap_socket(self.sock,
                                            server_side=True,
                                            certfile="certificates\server\server.pem",
                                            keyfile='certificates\server\server.key')
            print self.name + ' Connected with ' + addr[0] + ':' + str(addr[1])
            try:
                data = json.loads(self.ssl_sock.recv(4096))  # load from json (json is used for serialization)
                if not data:
                    break
                recv = data[1]
                print self.name + " [DEBUG] Received data from client: " + str(data)
                crypt = str(data[0][0]).split('-')  # AES256-SHA -> AES256 SHA
                print "%s SSL Version: %s" % (self.name, str(data[0][1]))
                print "%s Using %s as encryption algorithm & %s as integrity protection algorithm " \
                      % (self.name, crypt[0], crypt[1])
                # sending & receiving the data
                reply = "lulz the for"
                self.ssl_sock.sendall(reply)

                # xor strings to create a master key
                print "%s Creating new master key, xor: \'%s\' & \'%s\'" % (self.name, recv, reply)
                self.master = bin((int(binascii.hexlify(recv), 16)) ^ int(binascii.hexlify(reply), 16))

                # Computes a hash out of the msgs sent & received + the string "SERVER"
                hash_sha1 = hashlib.sha1(recv + reply + "SERVER")
                hex_dig = hash_sha1.hexdigest()
                print "%s SHA1 hash created: %s" % (self.name, hex_dig)
                client_hex = self.ssl_sock.recv(2048)
                if not client_hex:
                    break
                # Verify the client hash
                if client_hex == hashlib.sha1(recv + reply + "CLIENT").hexdigest():
                    print "%s Client hash verified" % self.name
                else:
                    print "%s Client didn't receive all msgs correctly" % self.name
                self.ssl_sock.sendall(hex_dig)  # send the server hash to client

                self.myssl_pubkey_server()

            finally:
                self.ssl_sock.shutdown(socket.SHUT_RDWR)
                self.ssl_sock.close()

    def myssl_symmetric_server(self):
        #generate the RSA key
        """


        """
        # tmp = binascii.
        # rsakey = RSA.generate(512, self.master.get_bytes)
        # print RSA.generate(512, self.master.get_bytes)
        # print RSA.generate(512, self.master.get_bytes)
        # print RSA.generate(512, self.master.get_bytes)
        print Random.new().read
        # rsapubkey = rsakey.publickey()
        #
        # #send the public key over
        # self.ssl_sock.send(json.dumps(rsapubkey))
        #
        # rcstring = ''
        # while 1:
        #     buf = self.ssl_sock.recv(1024)
        #     rcstring += buf
        #     if not len(buf):
        #       break
        # #encmessage is the cipher text
        # encmessage = pickle.loads(rcstring)
        #
        #   print rsakey.decrypt(encmessage)


Bob = MySSLServer("[Bob]")
Bob.start_server()
Bob.myssl_cert_server()