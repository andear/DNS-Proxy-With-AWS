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
    except socket.error, msg:
        print 'TCP socket bind failed.'
        sys.exit()

    tcpsocket.listen(10)
    print "TCP socket now listening"

    udpsocket = socket(AF_INET, SOCK_DGRAM)
    print 'UDP socket created'

    try:
        udpsocket.bind((host, 53))
        print 'UDP socket bind succeed.'
    except socket.error, msg:
        print 'UDP socket bind failed.'
        sys.exit()

    inputs = [tcpsocket, udpsocket]

    while True:
        readable, writable, exceptional = select(inputs, [], [])

        for sock in readable:
            if sock == tcpsocket:
                connection, address = sock.accept()
                request = connection.recv(1024)
                print "TCP recved."
                tcpresponse = getTCPResponse(request)
                print "TCP Responsed"

                connection.sendall(tcpresponse)
                connection.close()
                # inputs.append(connection)

            elif sock == udpsocket:
                data, address = sock.recvfrom(1024)
                # print data.encode("hex"), address

                udpresponse = getUDPResponse(data)
                print "UDP Responsed"

                sock.sendto(udpresponse, address)
            else:
                print "incorrect socket:", sock


def getTCPResponse(query):
    '''
    Get TCP response from upstream DNS server
    :param query: TCP query going to be sent
    :return:
    '''
    upstreamServer = ('8.8.8.8', 53)
    querysocket = socket(AF_INET, SOCK_STREAM)
    querysocket.connect(upstreamServer)
    querysocket.sendall(query)
    try:
        data = querysocket.recv(5000)
    except Exception, timeout:
        print "Request time out"
    return data


def getUDPResponse(query):
    '''
    Get UDP response from upstream DNS server
    :param query: UDP query going to be sent
    :return:
    '''
    upstreamServer = ('8.8.8.8', 53)
    querysocket = socket(AF_INET, SOCK_DGRAM)
    querysocket.sendto(query, upstreamServer)
    try:
        data, add = querysocket.recvfrom(1024)
    except Exception, timeout:
        print "Request time out"
    return data


if __name__ == '__main__':

    DNSProxy()

    sys.exit(0)
