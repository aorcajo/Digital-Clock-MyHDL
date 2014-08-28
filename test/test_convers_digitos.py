# -*- coding: utf-8 -*-

import unittest

from myhdl import *

from utils.clockdriver import clockDriver
from genticks import GenTicks
from convers_digitos import Conver_digitos


clk_period = 2
tick_period = 2


def trace(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg, tick_period):

    # tick = Signal(0)
    reloj = Conver_digitos(clk, nrst, ena, hora, min, seg, dig_seg, dig0, dig1, dig2, dig3)
    tick = GenTicks(clk, nrst, tick, tick_period)

    return reloj, tick


def runSim(test, num_it):
    clk, ajuste, ajuste_hora, ajuste_min, ajuste_seg, ena = [Signal(bool(0)) for i in range(6)]

    clock = clockDriver(clk, clk_period)
    nrst = ResetSignal(1, active=0, async=True)

    hora = Signal(intbv(0, min=0, max=24))
    min = Signal(intbv(0, min=0, max=60))
    seg = Signal(intbv(0, min=0, max=60))

    dig_seg, dig0, dig1, dig2, dig3 = [Signal(intbv(0, min=0, max=10)) for i in range(5)]

    dut = Conver_digitos(clk, nrst, ena, hora, min, seg, dig_seg, dig0, dig1, dig2, dig3)
    #dut = traceSignals(trace, clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg, tick_period)
    check = test(clk, nrst, ena, hora, min, seg, dig_seg, dig0, dig1, dig2, dig3)
    sim = Simulation(clock, dut, check)
    sim.run(num_it, quiet=1)


class TestSincronizador(unittest.TestCase):

    def test_basico(self):
        """* Comprueba el funcionamiento básico del coversor"""

        def test(clk, nrst, ena, hora, min, seg, dig_seg, dig0, dig1, dig2, dig3):
            ena.next = 1
            for h in range(24):
                hora.next = h
                for m in range(60):
                    min.next = m
                    for s in range(60):
                        seg.next = s
                        yield delay(tick_period*2)
                        self.assertEqual(h // 10, dig0)
                        self.assertEqual(h % 10, dig1)
                        self.assertEqual(m // 10, dig2)
                        self.assertEqual(m % 10, dig3)
                        self.assertEqual(s // 6, dig_seg)

        runSim(test, 60*60*24*tick_period)


if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
