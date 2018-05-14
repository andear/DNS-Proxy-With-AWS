import sys
from DNS import DNS
from socket import *
from select import select

def DNSProxy():
    # AD = "18.222.87.126" -> '\x12\xde\x57\x7e'
    # WH =  18.188.73.52   -> '\x12\xbc\x49\x34'

    # MyIP = [b'\x12',b'\xbc',b'\x49',b'\x34']
    MyIP = b'\x12\xde\x57\x7e'

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
                responsebuffer = []
                while True:
                    data = querysocket.recv(1024)
                    print "TCP request sent"
                    if data:
                        responsebuffer.append(data)
                        print "TCP Responsed"
                    else:
                        break
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

                respond_DNS = DNS(udpresponse)

                if respond_DNS.is_error():
                    udpresponse = respond_DNS.fake_an_answer(MyIP)

                sock.sendto(udpresponse, address)
            else:
                print "incorrect socket:", sock


if __name__ == '__main__':

    DNSProxy()

    sys.exit(0)


