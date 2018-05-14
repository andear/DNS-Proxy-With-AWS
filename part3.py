from socket import *
import sys
from select import select

def DNSProxy():
    host = ''
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    print 'TCP socket created'

    try:
        tcpsocket.bind((host, 53))
        print 'TCP socket bind succeed.'
    except Exception, msg:
        print 'TCP socket bind failed.'
        sys.exit()

    tcpsocket.listen(10)
    print "TCP socket now listening"

    udpsocket = socket(AF_INET, SOCK_DGRAM)
    print 'UDP socket created'

    try:
        udpsocket.bind((host, 53))
        print 'UDP socket bind succeed.'
    except Exception, msg:
        print 'UDP socket bind failed.'
        sys.exit()

    inputs = [tcpsocket, udpsocket]

    while True:
        readable, writable, exceptional = select(inputs, [], [])

        for sock in readable:
            if sock == tcpsocket:
                connection, address = sock.accept()
                request = connection.recv(4096)
                print(request)
                print "TCP request recved."

                upstreamServer = ('8.8.8.8', 53)
                querysocket = socket(AF_INET, SOCK_STREAM)
                querysocket.connect(upstreamServer)
                querysocket.sendall(request)
                empty = False
                while True:
                    tcpresponse = querysocket.recv(1024)
                    print "TCP request sent"
                    if tcpresponse:
                        connection.sendall(tcpresponse)
                        print "TCP Responsed"
                    else:
                        if not empty:
                            empty = True
                            continue
                        else :
                            break

                querysocket.close()

                connection.close()

            elif sock == udpsocket:
                data, address = sock.recvfrom(1024)
                # print data.encode("hex"), address
                upstreamServer = ('8.8.8.8', 53)
                # querysocket = socket(AF_INET, SOCK_DGRAM)
                sock.sendto(data, upstreamServer)

                udpresponse, add = sock.recvfrom(1024)
                print "UDP Responsed"

                sock.sendto(udpresponse, address)
            else:
                print "incorrect socket:", sock


if __name__ == '__main__':

    DNSProxy()

    sys.exit(0)
