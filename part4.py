import socket
import sys
from DNS import DNS

def UDPDNSProxy():

    # AD = "18.222.87.126" -> '\x12\xde\x57\x7e'
    # WH =  18.188.73.52   -> '\x12\xbc\x49\x34'

    MyIP = b'\x12\xbc\x49\x34'
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
        print data.encode("hex"), address

        response = getResponse(data)
        respond_DNS = DNS(response)

        if respond_DNS.is_error():
            response = respond_DNS.fake_an_answer(MyIP)

        print "get response"

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
    try :
        data, add = querysocket.recvfrom(1024)
    except Exception, timeout:
        print "Request time out"
    return data


if __name__ == '__main__':

    UDPDNSProxy()

    sys.exit(0)
