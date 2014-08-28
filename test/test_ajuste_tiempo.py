# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import unittest
from myhdl import *

from utils.clockdriver import clockDriver
from ajuste_tiempo import Ajuste_tiempo

clk_period = 2
tick_period = 2


def trace(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg):
    # tick = Signal(0)
    ajuste = Ajuste_tiempo(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg)

    return ajuste


def runSim(test, num_it):
    clk, ajuste, but1_s, but2_s, sw0_s = [Signal(bool(0)) for i in range(5)]

    clock = clockDriver(clk, clk_period)
    nrst = ResetSignal(1, active=0, async=True)

    hora, ajuste_hora = [Signal(intbv(0, min=0, max=24)) for i in range(2)]
    min, seg, ajuste_min, ajuste_seg = [Signal(intbv(0, min=0, max=60)) for i in range(4)]

    dut = Ajuste_tiempo(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg)
    #dut = traceSignals(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg)
    check = test(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg)
    sim = Simulation(clock, dut, check)
    sim.run(num_it, quiet=1)


class TestSincronizador(unittest.TestCase):

    def test_basico(self):
        """* Comprueba el funcionamiento básico del ajuste del tiempo"""

        def test(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg):
            hora.next = 22
            min.next = 58
            seg.next = 32
            yield delay(tick_period*4)
            self.assertEqual(ajuste, 0)

            sw0_s.next = 0
            yield delay(tick_period*4)
            self.assertEqual(ajuste, 0)

            sw0_s.next = 1
            yield delay(tick_period*4)
            self.assertEqual(ajuste, 1)
            self.assertEqual(ajuste_hora, hora)
            self.assertEqual(ajuste_min, min)
            self.assertEqual(ajuste_seg, seg)

            but2_s.next = 1
            yield delay(tick_period*4)
            self.assertEqual(ajuste, 1)
            self.assertEqual(ajuste_hora, hora)
            self.assertEqual(ajuste_min, (min+1) % 60)
            self.assertEqual(ajuste_seg, 0)

            hora.next = ajuste_hora
            min.next = ajuste_min
            seg.next = ajuste_seg

            but1_s.next = 1
            but2_s.next = 0
            yield delay(tick_period*4)
            self.assertEqual(ajuste, 1)
            self.assertEqual(ajuste_hora, (hora+1) % 24)
            self.assertEqual(ajuste_min, min)
            self.assertEqual(ajuste_seg, seg)

            hora.next = ajuste_hora
            min.next = ajuste_min
            seg.next = ajuste_seg
            but1_s.next = 0
            yield delay(tick_period*4)

            but2_s.next = 1
            but1_s.next = 1

            yield delay(tick_period*4)
            self.assertEqual(ajuste, 1)
            self.assertEqual(ajuste_hora, (hora+1) % 24)
            self.assertEqual(ajuste_min, (min+1) % 60)
            self.assertEqual(ajuste_seg, 0)

            hora.next = ajuste_hora
            min.next = ajuste_min
            seg.next = ajuste_seg

            yield delay(tick_period*4)
            self.assertEqual(ajuste, 1)
            self.assertEqual(ajuste_hora, hora % 24)
            self.assertEqual(ajuste_min, min % 60)
            self.assertEqual(ajuste_seg, 0)

            sw0_s.next = 1
            but2_s.next = 1
            but1_s.next = 1

            yield delay(tick_period*4)
            self.assertEqual(ajuste, 1)
            self.assertEqual(ajuste_hora, hora % 24)
            self.assertEqual(ajuste_min, min % 60)
            self.assertEqual(ajuste_seg, 0)

        runSim(test, 512)



if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
