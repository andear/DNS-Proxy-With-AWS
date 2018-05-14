import socket
import sys
import re
import time

def server1(port):
    host = ''

    # create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    try:
        # bind the socket to the port
        s.bind((host, port))
    except socket.error, msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    # listen on the accept socket
    s.listen(10)
    print "The accept socket now listening"

    while True:
        # wait to accept a connection
        connection, address = s.accept()
        print 'Connected with ' + address[0] + ':' + str(address[1])

        request = connection.recv(1024)
        method = request.split(' ')[0]
        if method == 'GET':
            response = constructNotFoundResponse(request)
            connection.sendall(response)

        else :
            print "Not a GET request."

        connection.close()

    s.close()



def constructHTTPHeader(responseData, responseCode):
    '''
    construct HTTP header
    :param responseData:
    :param responseCode:
    :return:
    '''
    header = ''
    if responseCode == 200:
        header += 'HTTP/1.1 200 OK\r\n'
        header += 'Content-Type: text/html\r\n'
    elif responseCode == 404:
        header += 'HTTP/1.1 404 Not Found\r\n'
    elif responseCode == 403:
        header += 'HTTP/1.1 403 Forbidden\r\n'

    time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    header += 'Date: {now}\r\n'.format(now=time_now)
    header += 'Server: Simple-Python-Server\r\n'
    length = len(responseData)
    header += 'content-length: %d\r\n' % length
    header += 'Connection: close\r\n\r\n'
    # Signal that connection will be closed after completing the request
    return header


def constructNotFoundResponse(receiveData):
    '''
    construct 404 Response
    :param receiveData:
    :return:
    '''
    domain = getDomain(receiveData)

    responseData = ''
    if receiveData.split(' ')[0] == 'GET':
        first= b"<html><body><center><h1>"
        message = "Cannot find host: " + domain + ", Try to google the right name"
        last = "</h1></center></body></html>"

        responseData = first + message + last
        responseData = responseData.encode()
    responseHeader = constructHTTPHeader(responseData, 404)
    response = responseHeader.encode()
    response += responseData
    return response



def getDomain(request):

    domain = "test"
    searchObj = re.search(r'(.*)Host: (.*?)\r\n.*', request, re.M | re.I)
    if searchObj is not None:
        domain = searchObj.group(2)
    return domain

if __name__ == '__main__':

    server1(80);

    sys.exit(0)