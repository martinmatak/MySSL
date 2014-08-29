MySSL - SSL Client &amp; Server with self signed CA
=====

The goal of this assignment is to build your own simplified version of SSL, called mySSL.
Uses client/server sockets to create a TCP connection.
The client server programs do the following:

1.  Handshake:

    * The client and the server authenticate each other using certificates. You need to create the
    certificates and include them in the mySSL messages.
    * The client also informs the server what data encryption and integrity protection scheme to use
    (there is no negotiation). Pick your favorite integrity protection and encryption algorithms.
    * The client and server also send encrypted nonces to each other. These nonces are then xored
    to create a master secret.
    * Compute a hash of all messages exchanged at both the client and server and exchange these
    hashes. Use keyed SHA-1 for computing the hash. The client appends the string CLIENT for
    computing its keyed hash and the server appends the string SERVER for computing its keyed
    hash. Verify the keyed hashes at the client and the server.
    * Generate four keys (two each for encryption, authentication, in each direction of the
    communication between the client and the server) using this master secret. Pick your own key
    generation function (should be a function of the master secret).

2.  Data Phase:

    * Use the SSL record format and securely transfer a file, at least 50 Kbytes long file, from the
    server to client.
    * Decrypt the file at the client and do a diff of the original and the decrypted file to ensure that
    the secure file transfer was successful.



1. CA - self signed with a private key (proteced by a pass)
1. Client - Alice (client
2. Server - Bob


Using OpenSSL:
=====

    Generating Client/Server certificates with a local CA
    Using these certificate/key pairs with nettest
    Copied from: http://www.devsec.org/info/ssl-cert.html

****************************************************************************
Generating Client/Server certificates with a local CA
*make sure openssl points to the correct instillation (%which openssl).  Mine is aliased to /usr/local/openssl/bin/openssl

Generate a CA & Sign request
1)    openssl req -out ca.pem -new -x509
      -generates CA file "ca.pem" and CA key "privkey.pem"

Generate server certificate/key pair
      - no password required.
2)    openssl genrsa -out server.key 1024
3)    openssl req -key server.key -new -out server.req
4)    openssl x509 -req -in server.req -CA CA.pem -CAkey privkey.pem -CAcreateserial -out server.pem
       -contents of "ca.srl" (created by the CAcreateserial command) is a two digit number.  eg. "00"

Generate client certificate/key pair

5)    Either choose to encrypt the key(a) or not(b)
        a. Encrypt the client key with a passphrase
            openssl genrsa -des3 -out client.key 1024
        b. Don't encrypt the client key
            openssl genrsa -out client.key 1024
6)    openssl req -key client.key -new -out client.req
7)    openssl x509 -req -in client.req -CA CA.pem -CAkey privkey.pem -CAserial file.srl -out client.pem
        -contents of "file.srl" is a two digit number.  eg. "00"

8)    DONE