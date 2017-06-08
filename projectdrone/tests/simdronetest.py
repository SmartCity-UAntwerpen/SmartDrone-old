import unittest
from projectdrone.core.coreDrone import coreDrone
import time
from threading import Thread

class CoreTest(unittest.TestCase):

    def setUp(self):
        print 'In setUp()'
        Thread(target=coreDrone(), args=()).start()

    def tearDown(self):
        pass#del self.thread

    def test_MakeSimDrone(self):
        self.failIf(0)
        pass
        self.failUnlessEqual("ACK\n", self.core.simcore.create_drone(1))
        self.failUnlessEqual("NACK\n", self.core.simcore.run_drone(1))

        self.failIfEqual("NACK\n", self.core.simcore.set_drone_startpoint(1, 44))
        self.failIfEqual("ACK\n", self.core.simcore.set_drone_startpoint(2, 44))

if __name__ == '__main__':
    unittest.main()