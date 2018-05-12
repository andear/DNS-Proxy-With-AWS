class Header:
    def __init__(self,bytes):
        self.byte_ID = [bytes[0],bytes[1]]
        self.byte_flags = [bytes[2],bytes[3]]
        self.byte_queryNum = [bytes[4],bytes[5]]
        self.byte_answerNum = [bytes[6],bytes[7]]
        self.byte_authoNum = [bytes[8],bytes[9]]
        self.byte_additionNum = [bytes[10],bytes[11]]

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
    def __init__(self,bytes,n):
        list = []
        for i in range(n+1):
            list.append(bytes[i])

        self.byte_domain = list
        self.byte_type = [bytes[n+1],bytes[n+2]]   #type A should be 1
        self.byte_category = [bytes[n+3],bytes[n+4]]

    def to_bytes_array(self):
        res = []
        res.extend(self.byte_domain)
        res.extend(self.byte_type)
        res.extend(self.byte_category)

        return res

class Answer:
    def __init__(self):
        self.byte_domain = []
        self.byte_type = []
        self.byte_category = []
        self.byte_ttl = []
        self.byte_length = []
        self.byte_Cname = []

    def to_bytes_array(self):
        res = []
        res.extend(self.byte_domain)
        res.extend(self.byte_type)
        res.extend(self.byte_category)
        res.extend(self.byte_ttl)
        res.extend(self.byte_length)
        res.extend(self.byte_Cname)

        return res



class DNS:
    def __init__(self,bytes):
        self.header = Header(bytes)

        self.queryNum = self.__convert_to_integer(self.header.byte_queryNum)
        self.answerNum = self.__convert_to_integer(self.header.byte_answerNum)
        self.authoNum = self.__convert_to_integer(self.header.byte_authoNum)
        self.additionNum = self.__convert_to_integer(self.header.byte_additionNum)

        bytes = bytes[12:]

        offset = self.__construct_queries(bytes)
        bytes = bytes[offset:]

        offset = self.__construct_answers(bytes)
        bytes = bytes[offset:]

        self.rest = bytes


    def __construct_queries(self,bytes):
        n = self.queryNum

        self.queries = []
        num_bytes = 0
        return num_bytes

    def __construct_answers(self,bytes):
        self.answers = []
        num_bytes = 0
        return num_bytes


    def __convert_to_integer(self,input):
        res = ord(input[0])
        res = res * 256 + ord(input[1])
        return res

    def to_bytes_array(self):
        res = []
        res.extend(self.header.to_bytes_array())
        for query in self.queries:
            res.extend(query.to_bytes_array())
        for answer in self.answers:
            res.extend(answer.to_bytes_array())
        res.extend(self.rest)
        return res

