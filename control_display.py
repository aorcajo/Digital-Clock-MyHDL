from myhdl import *

from utils.leds import leds_st, encoding


def Control_display(clk, nrst, tic, dig_seg, dig0, dig1, dig2, dig3, leds, dis0, dis1, dis2, dis3):

    return (Ctrl_disp(clk, nrst, tic, dig0, dis0), Ctrl_disp(clk, nrst, tic, dig1, dis1),
            Ctrl_disp(clk, nrst, tic, dig2, dis2), Ctrl_disp(clk, nrst, tic, dig3, dis3),
            Ctrl_leds(clk, nrst, tic, dig_seg, leds))


def Ctrl_leds(clk, nrst, tic, dig_seg, leds):
    @always_seq(clk.posedge, reset=nrst)
    def ctrl_leds():
        if tic:
            leds.next = leds_st[int(dig_seg)]

    return ctrl_leds


def Ctrl_disp(clk, nrst, tic, dig, disp):
    @always_seq(clk.posedge, reset=nrst)
    def ctrl_disp():
        if tic:
            disp.next = encoding[int(dig)]

    return ctrl_disp