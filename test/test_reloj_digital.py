# -*- coding: utf-8 -*-

import unittest

from myhdl import *

from utils.clockdriver import clockDriver
from reloj_digital import Reloj_Digital
from utils.leds import encoding, leds_st

clk_period = 2
tick_period = 2


def print_hora(dis0, dis1, dis2, dis3):
    print '{0}{1}:{2}{3}'.format(str(encoding.index(dis0)), str(encoding.index(dis1)),
                                 str(encoding.index(dis2)), str(encoding.index(dis3)))


def disp_num(dis0, dis1):
    return encoding.index(dis0)*10 + encoding.index(dis1)


def runSim(test, num_it):
    clk, tic, ena = [Signal(bool(0)) for i in range(3)]

    clock = clockDriver(clk, clk_period)
    nrst = ResetSignal(1, active=0, async=True)

    sw0, but1, but2 = [Signal(bool(0)) for i in range(3)]
    dis0, dis1, dis2, dis3 = [Signal(intbv(0)[8:]) for i in range(4)]
    leds = Signal(intbv(0)[10:])

    dut = Reloj_Digital(clk, nrst, sw0, but1, but2, leds, dis0, dis1, dis2, dis3, tick_period)
    check = test(clk, nrst, sw0, but1, but2, leds, dis0, dis1, dis2, dis3, tick_period)
    sim = Simulation(clock, dut, check)
    sim.run(num_it, quiet=1)


class TestSincronizador(unittest.TestCase):

    def test_basico(self):
        """* Comprueba el funcionamiento básico del reloj"""

        test_hours = 25

        def test(clk, nrst, sw0, but1, but2, leds, dis0, dis1, dis2, dis3, period):
            yield delay(tick_period*2)
            for h in range(test_hours):
                for m in range(60):
                    for s in range(60):
                        yield delay(tick_period*2)
                        hh = h % 24
                        self.assertEqual(leds, leds_st[s // 6])
                        self.assertEqual(dis0, encoding[hh // 10])
                        self.assertEqual(dis1, encoding[hh % 10])
                        self.assertEqual(dis2, encoding[m // 10])
                        self.assertEqual(dis3, encoding[m % 10])
                    #print_hora(dis0, dis1, dis2, dis3)

        runSim(test, 60*60*test_hours*tick_period*2)

    def test_ajuste(self):
        """* Comprueba el funcionamiento del ajuste de tiempo"""

        def test(clk, nrst, sw0, but1, but2, leds, dis0, dis1, dis2, dis3, period):
            #yield delay(tick_period * 2 * randrange(120))

            sw0.next = 1
            yield delay(tick_period*4)

            m = 0
            h = 0

            for i in range(62*2):
                but2.next = not but2
                yield delay(tick_period*4)

                if but2:
                    #print_hora(dis0, dis1, dis2, dis3)
                    self.assertEqual(disp_num(dis0, dis1), h)
                    self.assertEqual(disp_num(dis2, dis3), m)
                    m = (m + 1) % 60

            for i in range(25*2):
                but1.next = not but1
                yield delay(tick_period*4)

                if but1:
                    #print_hora(dis0, dis1, dis2, dis3)
                    self.assertEqual(disp_num(dis0, dis1), h)
                    self.assertEqual(disp_num(dis2, dis3), m)
                    h = (h + 1) % 24

            sw0.next = 0
            yield delay(tick_period*4)


        runSim(test, 2024*tick_period)

if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
