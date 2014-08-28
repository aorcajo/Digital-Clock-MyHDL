import os
import shutil
from myhdl import *

from ajuste_tiempo import Ajuste_tiempo
from control_display import Control_display
from convers_digitos import Conver_digitos
from genticks import GenTicks
from reloj import Reloj
from sincronizador import Sincronizador


def Reloj_Digital(clk, nrst, sw0, but1, but2, leds, dis0, dis1, dis2, dis3, period=2):

    sw0_s, but1_s, but2_s, tic, ena, ajuste = [Signal(bool(0)) for i in range(6)]
    hora, ajuste_hora = [Signal(intbv(0, min=0, max=24)) for i in range(2)]
    min, seg, ajuste_min, ajuste_seg = [Signal(intbv(0, min=0, max=60)) for i in range(4)]
    dig_seg, dig0, dig1, dig2, dig3 = [Signal(intbv(0, min=0, max=10)) for i in range(5)]

    @always(clk.posedge)
    def OR():
        ena.next = tic or but1_s or but2_s

    gen_tic = GenTicks(clk, nrst, tic, period)
    sincronizador = Sincronizador(clk, nrst, sw0, but1, but2, sw0_s, but1_s, but2_s)
    reloj = Reloj(clk, nrst, tic, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg)
    ajuste_tiempo = Ajuste_tiempo(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg)
    conversor_digitos = Conver_digitos(clk, nrst, ena, hora, min, seg, dig_seg, dig0, dig1, dig2, dig3)
    control_displays = Control_display(clk, nrst, ena, dig_seg, dig0, dig1, dig2, dig3, leds, dis0, dis1, dis2, dis3)

    return sincronizador, gen_tic, OR, reloj, ajuste_tiempo, conversor_digitos, control_displays


if __name__ == '__main__':
    clk = Signal(bool(0))
    nrst = ResetSignal(1, active=0, async=True)

    sw0, but1, but2 = [Signal(bool(0)) for i in range(3)]
    dis0, dis1, dis2, dis3 = [Signal(intbv(0)[7:]) for i in range(4)]
    leds = Signal(intbv(0)[10:])

    inc_inst = toVHDL(Reloj_Digital, clk, nrst, sw0, but1, but2, leds, dis0, dis1, dis2, dis3, 50000000)

    for f in os.listdir('.'):
        if os.path.isfile(f) and f.endswith(".vhd"):
            shutil.move(f, "vhdl/"+f)