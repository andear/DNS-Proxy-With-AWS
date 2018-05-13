import socket
import sys

def UDPDNSProxy(port):
    host = ''
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'

    try:
        udpsocket.bind((host, port))
        print 'Bind succeed.'
    except socket.error, msg:
        print 'Bind failed.'
        sys.exit()

    while True:
        data, address = udpsocket.recvfrom(1024)
        print data.encode("hex"), address

        response = getResponse(data)
        print "answer:", response.encode("hex")

        if response:
            udpsocket.sendto(response, address)
        else:
            print "Not a DNS query."


def getResponse(query):
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
    UDPDNSProxy(port)

    sys.exit(0)
