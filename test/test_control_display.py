# -*- coding: utf-8 -*-

import unittest

from myhdl import *

from utils.clockdriver import clockDriver
from genticks import GenTicks
from control_display import Control_display
from utils.leds import leds_st, encoding


clk_period = 2
tick_period = 2


def trace(clk, nrst, tic, dig_seg, dig0, dig1, dig2, dig3, leds, dis0, dis1, dis2, dis3):
    # tick = Signal(0)
    reloj = Control_display(clk, nrst, tic, dig_seg, dig0, dig1, dig2, dig3, leds, dis0, dis1, dis2, dis3)
    tick = GenTicks(clk, nrst, tic, tick_period)

    return reloj, tick


def runSim(test, num_it):
    clk, tic, ena = [Signal(bool(0)) for i in range(3)]

    clock = clockDriver(clk, clk_period)
    nrst = ResetSignal(1, active=0, async=True)

    dig_seg, dig0, dig1, dig2, dig3 = [Signal(intbv(0, min=0, max=10)) for i in range(5)]
    dis0, dis1, dis2, dis3 = [Signal(intbv(0)[8:]) for i in range(4)]
    leds = Signal(intbv(0)[10:])

    ticks = GenTicks(clk, nrst, tic, tick_period)
    dut = Control_display(clk, nrst, ticks, dig_seg, dig0, dig1, dig2, dig3, leds, dis0, dis1, dis2, dis3)
    #dut = traceSignals(trace, clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg, tick_period)
    check = test(clk, nrst, tic, dig_seg, dig0, dig1, dig2, dig3, leds, dis0, dis1, dis2, dis3)
    sim = Simulation(clock, dut, check)
    sim.run(num_it, quiet=1)


class TestSincronizador(unittest.TestCase):

    def test_basico(self):
        """* Comprueba el funcionamiento básico del coversor"""

        def test(clk, nrst, tic, dig_seg, dig0, dig1, dig2, dig3, leds, dis0, dis1, dis2, dis3):
            for h in range(24):
                dig0.next = h // 10
                dig1.next = h % 10
                for m in range(60):
                    dig2.next = m // 10
                    dig3.next = m % 10
                    for s in range(60):
                        dig_seg.next = s // 6
                        yield delay(tick_period*2)
                        self.assertEqual(leds, leds_st[int(dig_seg)])
                        self.assertEqual(dis0, encoding[int(dig0)])
                        self.assertEqual(dis1, encoding[int(dig1)])
                        self.assertEqual(dis2, encoding[int(dig2)])
                        self.assertEqual(dis3, encoding[int(dig3)])

        runSim(test, 60*60*24*tick_period)



if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
