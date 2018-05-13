import socket
import sys


def DNSProxy(port):
    host = ''
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'UDP socket created'

    try:
        udpsocket.bind((host, port))
        print 'UDP socket bind succeed.'
    except socket.error, msg:
        print 'UDP socket bind failed.'
        sys.exit()

    tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'TCP socket created'

    try:
        tcpsocket.bind((host, port))
        print 'TCP socket bind succeed.'
    except socket.error, msg:
        print 'TCP socket bind failed.'
        sys.exit()

    tcpsocket.listen(10)
    print "TCP socket now listening"

    while True:
        data, address = udpsocket.recvfrom(1024)
        print data.encode("hex"), address

        udpresponse = getUDPResponse(data)
        print "answer:", udpresponse.encode("hex")

        if udpresponse:
            udpsocket.sendto(udpresponse, address)
        else:
            print "Not a DNS query."


        connection, address = tcpsocket.accept()
        request = connection.recv(1024)
        
        tcpresponse = getTCPResponse(request)

        if tcpresponse:
            connection.sendall(tcpresponse)
            connection.close()
        else:
            print "Not a DNS query."

        

def getTCPResponse(query):
    '''
    Get TCP response from upstream DNS server
    :param query: TCP query going to be sent
    :return:
    '''
    upstreamServer = ('8.8.8.8', 53)
    querysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    querysocket.connect(upstreamServer)
    querysocket.send(query)
    data = querysocket.recv(1024)
    return data

def getUDPResponse(query):
    '''
    Get UDP response from upstream DNS server
    :param query: UDP query going to be sent
    :return:
    '''
    upstreamServer = ('8.8.8.8', 53)
    querysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    querysocket.sendto(query, upstreamServer)
    data = querysocket.recvfrom(1024)
    return data


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    port = int(sys.argv[1])
    DNSProxy(port)

    sys.exit(0)
