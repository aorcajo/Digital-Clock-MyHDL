# -*- coding: utf-8 -*-

import unittest
from random import randint

from myhdl import *

from utils.clockdriver import clockDriver
from genticks import GenTicks
from reloj import Reloj


clk_period = 2
tick_period = 2


def trace(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg, tick_period):
    # tick = Signal(0)
    reloj = Reloj(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg)
    tick = GenTicks(clk, nrst, tick, tick_period)

    return reloj, tick


def runSim(test, num_it):
    clk, tick, ajuste = [Signal(bool(0)) for i in range(3)]

    clock = clockDriver(clk, clk_period)
    nrst = ResetSignal(1, active=0, async=True)

    hora = Signal(intbv(0, min=0, max=24))
    min = Signal(intbv(0, min=0, max=60))
    seg = Signal(intbv(0, min=0, max=60))

    ajuste_hora = Signal(intbv(0, min=0, max=24))
    ajuste_min = Signal(intbv(0, min=0, max=60))
    ajuste_seg = Signal(intbv(0, min=0, max=60))

    tick = GenTicks(clk, nrst, tick, tick_period)
    dut = Reloj(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg)
    #dut = traceSignals(trace, clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg, tick_period)
    check = test(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg)
    sim = Simulation(clock, dut, check)
    sim.run(num_it, quiet=1)


class TestSincronizador(unittest.TestCase):

    def test_basico(self):
        """* Comprueba el funcionamiento básico del reloj"""

        def test(clk, nrst,tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg):
            for h in range(25):
                self.assertEqual(h % 24, hora)
                for m in range(60):
                    self.assertEqual(m, min)
                    for s in range(60):
                        self.assertEqual(s, seg)
                        yield delay(tick_period)

            self.assertEqual(1, hora)
            self.assertEqual(0, min)
            self.assertEqual(0, seg)

        runSim(test, 60*60*25*tick_period)

    def test_reset(self):
        """* Comprueba que con la señal de reset se reinicia"""

        def test(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg):
            for h in range(2):
                for m in range(60):
                    for s in range(60):
                        yield delay(tick_period)

            for s in range(randint(60, 180)):
                yield delay(tick_period)

            nrst.next = 0
            yield delay(clk_period)
            self.assertEqual(0, hora)
            self.assertEqual(0, min)
            self.assertEqual(0, seg)

            yield delay(randint(2, 80))
            nrst.next = 1
            yield delay(clk_period)
            self.assertEqual(0, hora)
            self.assertEqual(0, min)
            self.assertEqual(1, seg)

        runSim(test, 60*60*3*tick_period)

    def test_ajuste(self):
        """* Comprueba que con ajuste se cambia la hora"""

        def test(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg):

            yield delay(tick_period * randint(60, 180))
            ajuste.next = 1
            ajuste_hora.next = 5
            ajuste_min.next = 10
            ajuste_seg.next = 0

            yield delay(tick_period*2)
            self.assertEqual(5, hora)
            self.assertEqual(10, min)
            self.assertEqual(0, seg)

            ajuste.next = 0
            yield delay(tick_period)
            self.assertEqual(5, hora)
            self.assertEqual(10, min)
            self.assertEqual(1, seg)

        runSim(test, 60*60*3*tick_period)


if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
