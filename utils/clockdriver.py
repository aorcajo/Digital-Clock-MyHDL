from myhdl import *


def clockDriver(clk, period):

    halfPeriod = delay(period//2)

    @always(halfPeriod)
    def genClock():
        clk.next = not clk

    return genClock