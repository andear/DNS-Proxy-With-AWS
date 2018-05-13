#    +---------------------+
#    |        Header       |
#    +---------------------+
#    |       Question      | the question for the name server
#    +---------------------+
#    |        Answer       | RRs answering the question
#    +---------------------+
#    |      Authority      | RRs pointing toward an authority
#    +---------------------+
#    |      Additional     | RRs holding additional information
#    +---------------------+def QueryDNS(domain)
# :

def convert_two_bytes_to_integer(input):
    res = ord(input[0])
    res = res * 256 + ord(input[1])
    return res


class Header:
    def __init__(self,byte_array):
        self.byte_ID = [byte_array[0],byte_array[1]]
        self.byte_flags = [byte_array[2],byte_array[3]]
        self.byte_queryNum = [byte_array[4],byte_array[5]]
        self.byte_answerNum = [byte_array[6],byte_array[7]]
        self.byte_authoNum = [byte_array[8],byte_array[9]]
        self.byte_additionNum = [byte_array[10],byte_array[11]]

    def to_bytes_array(self):
        res = []
        res.extend(self.byte_ID)
        res.extend(self.byte_flags)
        res.extend(self.byte_queryNum)
        res.extend(self.byte_answerNum)
        res.extend(self.byte_authoNum)
        res.extend(self.byte_additionNum)

        return res

class Query:
    '''
       structure
       {
           byte_domain
           byte_type
           byte_category
           length
       }
    '''
    def __init__(self,byte_array,offset = 0):
        byte_array = byte_array[offset:]
        list = []
        n = 0

        while(ord(byte_array[n]) != 0):
            list.append(byte_array[n])
            n += 1

        list.append(byte_array[n])

        self.byte_domain = list
        self.byte_type = [byte_array[n+1],byte_array[n+2]]   #type A should be 1
        self.byte_category = [byte_array[n+3],byte_array[n+4]]

        self.length = n+5

    def to_bytes_array(self):
        res = []
        res.extend(self.byte_domain)
        res.extend(self.byte_type)
        res.extend(self.byte_category)

        return res


class Answer:
    '''
    structure
    {
       byte_domain
       byte_type
       byte_category
       byte_ttl
       byte_data_length
       byte_CnameOrIP: data
       length
    }
    '''

    def __init__(self,byte_array,offset = 0):
        byte_array = byte_array[offset:]

        self.byte_domain = [byte_array[0],byte_array[1]]  #offset of the domain
        self.byte_type = [byte_array[2],byte_array[3]]
        self.byte_category = [byte_array[4],byte_array[5]]
        self.byte_ttl = [byte_array[6],byte_array[7],byte_array[8],byte_array[9]]
        self.byte_data_length = [byte_array[10],byte_array[11]]

        data_length = convert_two_bytes_to_integer(self.byte_data_length)
        self.byte_CnameOrIP = []
        for i in range(data_length):
            index = i + 12
            self.byte_CnameOrIP.append(byte_array[index])

        self.length = 12 + data_length

    def to_bytes_array(self):
        res = []

        res.extend(self.byte_domain)
        res.extend(self.byte_type)
        res.extend(self.byte_category)
        res.extend(self.byte_ttl)
        res.extend(self.byte_data_length)
        res.extend(self.byte_CnameOrIP)

        return res


class DNS:
    '''
    structure
    {
        header
        queryNum
        answerNum
        queries
        answers
        rest
    }
    '''
    def __init__(self,byte_array):
        self.header = Header(byte_array)

        self.queryNum = convert_two_bytes_to_integer(self.header.byte_queryNum)
        self.answerNum = convert_two_bytes_to_integer(self.header.byte_answerNum)
        # self.authoNum = convert_two_bytes_to_integer(self.header.byte_authoNum)
        # self.additionNum = convert_two_bytes_to_integer(self.header.byte_additionNum)

        byte_array = byte_array[12:]

        self.queries = []
        self.answers = []

        offset = self.__construct_queries(byte_array)
        byte_array = byte_array[offset:]

        offset = self.__construct_answers(byte_array)
        byte_array = byte_array[offset:]

        self.rest = byte_array

    def __construct_queries(self,byte_array):
        n = self.queryNum
        offset = 0

        for i in range(n):
            query = Query(byte_array,offset)
            self.queries.append(query)
            offset += query.length

        return offset

    def __construct_answers(self,byte_array):
        n = self.answerNum
        offset = 0

        for i in range(n):
            answer = Answer(byte_array, offset)
            self.answers.append(answer)
            offset += answer.length

        return offset

    def to_bytes_array(self):
        '''
        convert the DNS object to a byte array,
        which can be directly sent by socket
        :return:
        '''
        res = []
        res.extend(self.header.to_bytes_array())
        for query in self.queries:
            res.extend(query.to_bytes_array())
        for answer in self.answers:
            res.extend(answer.to_bytes_array())
        # type(res) = list
        # convert list to sentable bytearray
        # [b'01',b'02'] --> b'\x01\x02'
        sentable = b''
        for i in res:
            sentable += i
        sentable += self.rest
        return sentable

    def is_error(self):
        '''
        see if there is an typo in the url
        :return:
        '''
        flag = self.header.byte_flags[1]
        rcode = ord(flag) & 15
        if rcode == 0:
            return False

        return True

    def fake_an_answer(self, MyIP):
        '''

        :param MyIP: 18.222.87.126  --> 0x12,0xde,0x57,0x7e
        :return:
        '''

        # change header, set rcode to 0
        self.header.byte_flags[1] = b'\x00'

        # change answer
        fake_answers = []

        domain = b'\xc0\x0c'
        answer_type = b'\x00\x01'  # type A, represent ip, not Cname
        category = b'\x00\x01'  #class IN
        ttl = b'\x00\x00\x00\x10'
        data_length = b'\x00\x04'  # for ip, the length is 4
        ip_address = MyIP

        flow = domain + answer_type + category + ttl + data_length + ip_address
        answer = Answer(flow)
        fake_answers.append(answer)
        self.answers = fake_answers

        return self.to_bytes_array()

