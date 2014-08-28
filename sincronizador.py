
from myhdl import *


def Sincronizador(clk, nrst, sw0, but1, but2, sw0_s, but1_s, but2_s):

    ffs_sw0 = Signal(intbv(0)[3:])
    ffs_but1 = Signal(intbv(0)[3:])
    ffs_but2 = Signal(intbv(0)[3:])

    @always_seq(clk.posedge, reset=nrst)
    def sincr_sw0():
        ffs_sw0.next = (ffs_sw0[2:] << 1) + sw0
        sw0_s.next = ffs_sw0[2]

    @always_seq(clk.posedge, reset=nrst)
    def sincr_but1():
        ffs_but1.next = (ffs_but1[2:] << 1) + but1
        but1_s.next = ffs_but1[2]

    @always_seq(clk.posedge, reset=nrst)
    def sincr_but2():
        ffs_but2.next = (ffs_but2[2:] << 1) + but2
        but2_s.next = ffs_but2[2]

    return sincr_sw0, sincr_but1, sincr_but2


if __name__ == '__main__':
    clk = Signal(bool(0))
    nrst = ResetSignal(1, active=0, async=True)
    sw0, but1, but2, sw0_s, but1_s, but2_s = [Signal(intbv(0, min=0, max=1)) for i in range(6)]

    inc_inst = toVHDL(Sincronizador, clk, nrst, sw0, but1, but2, sw0_s, but1_s, but2_s)