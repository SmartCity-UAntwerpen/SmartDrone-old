import unittest
import socket
from projectdrone.env import env
import time

class simdronetest(unittest.TestCase):

    def setUp(self):
        pass
        print 'In setUp()'
        HOST = env.tcpip # The remote host
        PORT = env.tcpport  # The same port as used by the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))


    def test_simdrone(self):
        print 'In Test()'
        self.s.send('create 37')
        data = self.s.recv(1024)
        string= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'NACK", string)

        self.s.send("run 1")#wrong set first startpoint
        data = self.s.recv(1024)
        print str(repr(data))
        data= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'NACK", data)

        self.s.send('set 1 startpoint 1')  # wrong idstartpoint
        data = self.s.recv(1024)
        data= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'NACK", data)

        self.s.send('set 1 startpoint 44')  # startpoint
        data = self.s.recv(1024)
        data= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'ACK", data)

        self.s.send('run 1')  # right
        data = self.s.recv(1024)
        data= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'ACK", data)

        self.s.send('set 1 startpoint 44')  # wrong drone running
        data = self.s.recv(1024)
        data= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'NACK", data)

        self.s.send('kill 1')  #right
        data = self.s.recv(1024)
        data= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'ACK", data)

        self.s.send('kill 2')  # wrong id
        data = self.s.recv(1024)
        data= str(repr(data)).split('\\', 1)[0]
        self.failUnlessEqual("'NACK", str(repr(data)))
        self.s.close()

if __name__ == '__main__':
    unittest.main()