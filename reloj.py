
from myhdl import *


def Reloj(clk, nrst, tick, ajuste, ajuste_hora, ajuste_min, ajuste_seg, hora, min, seg):

    @always_seq(clk.posedge, reset=nrst)
    def reloj():
        if ajuste:
            hora.next = ajuste_hora
            min.next = ajuste_min
            seg.next = ajuste_seg

        elif tick:
            if seg < 59:
                seg.next = seg + 1
            else:
                seg.next = 0

                if min < 59:
                    min.next = min + 1
                else:
                    min.next = 0
                    if hora < 23:
                        hora.next = hora + 1
                    else:
                        hora.next = 0


    return reloj