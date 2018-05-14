import socket
import sys

def UDPDNSProxy():
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'

    try:
        udpsocket.bind(('', 53))
        print 'Bind succeed.'
    except socket.error, msg:
        print 'Bind failed.'
        sys.exit()

    while True:
        data, address = udpsocket.recvfrom(1024)
        # print data.encode("hex"), address

        response = getResponse(data)
        print "Get response"

        udpsocket.sendto(response, address)


def getResponse(query):
    '''
    Get UDP response from upstream DNS server
    :param query: UDP query going to be sent
    :return:
    '''
    upstreamServer = ('8.8.8.8', 53)
    querysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    querysocket.sendto(query, upstreamServer)
    try :
        data, add = querysocket.recvfrom(1024)
    except Exception, timeout:
        print "Request time out"
    return data


if __name__ == '__main__':

    UDPDNSProxy()

    sys.exit(0)
