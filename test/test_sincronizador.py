# -*- coding: utf-8 -*-

import unittest

from myhdl import *

from sincronizador import Sincronizador
from ajuste_tiempo import Ajuste_tiempo
from utils.clockdriver import clockDriver


clk_period = 2


def runSim(test, num_it):
    clk = Signal(bool(0))
    clock = clockDriver(clk, clk_period)
    nrst = ResetSignal(1, active=0, async=True)
    sw0, but1, but2, sw0_s, but1_s, but2_s = [Signal(bool(0)) for i in range(6)]

    dut = Sincronizador(clk, nrst, sw0, but1, but2, sw0_s, but1_s, but2_s)
    check = test(clk, nrst, sw0, but1, but2, sw0_s, but1_s, but2_s)
    sim = Simulation(clock, dut, check)
    sim.run(num_it, quiet=1)


def Test_Sincro_Ajuste(clk, nrst, sw0, but1, but2, hora, ajuste_hora, min, seg, ajuste_min, ajuste_seg, ajuste):
    sw0_s, but1_s, but2_s = [Signal(bool(0)) for i in range(3)]

    sincronizador = Sincronizador(clk, nrst, sw0, but1, but2, sw0_s, but1_s, but2_s)
    ajuste_tiempo = Ajuste_tiempo(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg)

    return sincronizador, ajuste_tiempo


def runAdvSim(test, num_it):
    clk = Signal(bool(0))
    clock = clockDriver(clk, clk_period)
    nrst = ResetSignal(1, active=0, async=True)

    sw0, but1, but2, ajuste = [Signal(bool(0)) for i in range(4)]
    hora, ajuste_hora = [Signal(intbv(0, min=0, max=24)) for i in range(2)]
    min, seg, ajuste_min, ajuste_seg = [Signal(intbv(0, min=0, max=60)) for i in range(4)]

    dut = Test_Sincro_Ajuste(clk, nrst, sw0, but1, but2, hora, ajuste_hora, min, seg, ajuste_min, ajuste_seg, ajuste)
    check = test(clk, nrst, sw0, but1, but2, hora, ajuste_hora, min, seg, ajuste_min, ajuste_seg, ajuste)
    sim = Simulation(clock, dut, check)
    sim.run(num_it, quiet=1)


class TestSincronizador(unittest.TestCase):

    def test_basico(self):
        """* Comprueba el funcionamiento básico del sincronizador"""

        def test(clk, nrst, sw0, but1, but2, sw0_s, but1_s, but2_s):
            sw0.next = 0
            but1.next = 0
            but2.next = 0
            yield delay(4 * clk_period)
            self.assertEqual(0, sw0_s)
            self.assertEqual(0, but1_s)
            self.assertEqual(0, but2_s)

            sw0.next = 1
            but1.next = 0
            but2.next = 0
            yield delay(4 * clk_period)
            self.assertEqual(1, sw0_s)
            self.assertEqual(0, but1_s)
            self.assertEqual(0, but2_s)

            sw0.next = 0
            but1.next = 1
            but2.next = 0
            yield delay(4 * clk_period)
            self.assertEqual(0, sw0_s)
            self.assertEqual(1, but1_s)
            self.assertEqual(0, but2_s)

            sw0.next = 0
            but1.next = 0
            but2.next = 1
            yield delay(4 * clk_period)
            self.assertEqual(0, sw0_s)
            self.assertEqual(0, but1_s)
            self.assertEqual(1, but2_s)

            sw0.next = 1
            but1.next = 1
            but2.next = 1
            yield delay(4 * clk_period)
            self.assertEqual(1, sw0_s)
            self.assertEqual(1, but1_s)
            self.assertEqual(1, but2_s)

        runSim(test, 1000)

    def test_avanzado(self):
        """* Comprueba el funcionamiento del sincronizador junto al ajuste de tiempo"""

        def test(clk, nrst, sw0, but1, but2, hora, ajuste_hora, min, seg, ajuste_min, ajuste_seg, ajuste):
            sw0.next = 0
            but1.next = 0
            but2.next = 0

            hora.next = 22
            min.next = 58
            seg.next = 32

            yield delay(5 * clk_period)
            self.assertEqual(ajuste, 0)
            sw0.next = 1

            yield delay(5 * clk_period)
            self.assertEqual(ajuste, 1)

            h, m, s = hora, min, seg

            but1.next = 1
            yield delay(5 * clk_period)
            but1.next = 0
            h = (h+1) % 24
            yield delay(5 * clk_period)
            self.assertEqual(ajuste_hora, h)
            self.assertEqual(ajuste_min, m)
            self.assertEqual(ajuste_seg, s)

            but2.next = 1
            yield delay(5 * clk_period)
            but2.next = 0
            m = (m+1) % 60
            s = 0
            yield delay(5 * clk_period)
            self.assertEqual(ajuste_hora, h)
            self.assertEqual(ajuste_min, m)
            self.assertEqual(ajuste_seg, s)

            but1.next = 1
            but2.next = 1
            yield delay(5 * clk_period)
            but1.next = 0
            but2.next = 0
            m = (m+1) % 60
            h = (h+1) % 24
            s = 0
            yield delay(5 * clk_period)
            self.assertEqual(ajuste_hora, h)
            self.assertEqual(ajuste_min, m)
            self.assertEqual(ajuste_seg, s)

        runAdvSim(test, 200)


if __name__ == '__main__':
    testRunner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=testRunner)
