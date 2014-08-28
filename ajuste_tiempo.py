from myhdl import *


def Ajuste_tiempo(clk, nrst, but1_s, but2_s, sw0_s, hora, min, seg, ajuste, ajuste_hora, ajuste_min, ajuste_seg):

    captura, inc_hora, inc_min = [Signal(bool(0)) for i in range(3)]
    nff0, nff1, nff2 = [Signal(bool(1)) for i in range(3)]

    # Conformador de pulsos para el switch0
    @always_seq(clk.posedge, reset=nrst)
    def conf_sw():
        nff0.next = not sw0_s
        captura.next = sw0_s and nff0

    # Conformador de pulsos para el but2
    @always_seq(clk.posedge, reset=nrst)
    def conf_but1():
        nff1.next = not but1_s
        inc_hora.next = but1_s and nff1

    # Conformador de pulsos para el but2
    @always_seq(clk.posedge, reset=nrst)
    def conf_but2():
        nff2.next = not but2_s
        inc_min.next = but2_s and nff2

    @always_seq(clk.posedge, reset=nrst)
    def ajuste_tiempo():
        if captura:
            ajuste_hora.next = hora
            ajuste_min.next = min
            ajuste_seg.next = seg

        if sw0_s:
            ajuste.next = 1
            if inc_min and not captura:
                ajuste_min.next = (ajuste_min + 1) % 60
                ajuste_min.next = (ajuste_min + 1) % 60
                ajuste_seg.next = 0

            if inc_hora and not captura:
                ajuste_hora.next = (ajuste_hora + 1) % 24
        else:
            ajuste.next = 0

    return ajuste_tiempo, conf_sw, conf_but1, conf_but2