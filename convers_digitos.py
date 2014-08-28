from myhdl import *


def Conver_digitos(clk, nrst, ena, hora, min, seg, dig_seg, dig0, dig1, dig2, dig3):

    @always_seq(clk.posedge, reset=nrst)
    def conv_hora():
        if ena:
            dig0.next = hora // 10
            dig1.next = hora % 10

    @always_seq(clk.posedge, reset=nrst)
    def conv_min():
        if ena:
            dig2.next = min // 10
            dig3.next = min % 10


    @always_seq(clk.posedge, reset=nrst)
    def conv_seg():
        if ena:
            dig_seg.next = seg // 6

    return conv_hora, conv_min, conv_seg