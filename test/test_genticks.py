# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase

from myhdl import *

from genticks import GenTicks
from utils.clockdriver import clockDriver


MAX_WIDTH = 100


def runSim(test, num_it):
    for period in range(2, MAX_WIDTH):
        clk = Signal(bool(0))
        clock = clockDriver(clk, 2)
        nrst = ResetSignal(1, active=0, async=True)
        tick = Signal(bool(0))

        dut = GenTicks(clk, nrst, tick, period)
        check = test(clk, nrst, tick, period)
        sim = Simulation(clock, dut, check)
        sim.run(num_it, quiet=1)


class TestGenTicksProperties(TestCase):

    def testTickGenerator(self):
        """* Comprueba que genere bien los pulsos"""

        def test(clk, nrst, tick, period):
            yield delay(2)

            while True:
                yield delay(period*2 - 3)
                self.assertEqual(False, tick)
                yield delay(1)
                self.assertEqual(True, tick)
                yield delay(2)
                self.assertEqual(False, tick)

        runSim(test, 1000)

    def testReset(self):
        """* Comprueba que se reinicia con la señal de reset"""

        def test(clk, nrst, tick, period):
            yield delay(1)
            nrst.next = 0
            yield delay(1)
            nrst.next = 1
            yield delay(period*2-2)
            self.assertEqual(False, tick)
            yield delay(2)
            self.assertEqual(True, tick)
            nrst.next = 0
            yield delay(1)
            nrst.next = 1
            yield delay(period*2-2)
            self.assertEqual(False, tick)
            yield delay(2)
            self.assertEqual(True, tick)

        runSim(test, 300)

if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)