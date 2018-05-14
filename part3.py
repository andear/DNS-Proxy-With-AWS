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
                responsebuffer = []
                while True:
                    data = querysocket.recv(1024)
                    print "TCP request sent"
                    if data:
                        responsebuffer.append(data)
                        print "TCP Responsed"
                    else:
                        break
                        '''
                        if not empty:
                            empty = True
                            continue
                        else :
                            break
                    '''

                tcpresponse = ''.join(responsebuffer)
                connection.sendall(tcpresponse)

                querysocket.close()

                connection.close()

            elif sock == udpsocket:
                data, address = sock.recvfrom(1024)
                # print data.encode("hex"), address
                upstreamServer = ('8.8.8.8', 53)
                querysocket = socket(AF_INET, SOCK_DGRAM)
                querysocket.sendto(data, upstreamServer)

                udpresponse, add = querysocket.recvfrom(1024)
                print "UDP Responsed"

                sock.sendto(udpresponse, address)
            else:
                print "incorrect socket:", sock


if __name__ == '__main__':

    DNSProxy()

    sys.exit(0)
