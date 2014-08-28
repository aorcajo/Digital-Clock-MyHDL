from myhdl import *

from utils.clockdriver import clockDriver


def GenTicks(clk, nrst, tick, period):

    count = Signal(intbv(0, min=0, max=period))

    @always_seq(clk.posedge, reset=nrst)
    def genTicks():

        if count >= period-1:
            count.next = 0
            tick.next = True
            #print "%s tick" %now()
        else:
            count.next = count + 1
            tick.next = False

    return genTicks


def TestBench():
    clk = Signal(bool(0))
    clock = clockDriver(clk, 2)
    reset = ResetSignal(1, active=0, async=True)
    tick = Signal(bool(0))

    genticks = GenTicks(clk, reset, tick, 10)

    return clock, genticks

if __name__ == '__main__':
    inst = traceSignals(TestBench)
    sim = Simulation(inst)
    sim.run(1000)

    clock = Signal(bool(0))
    reset = ResetSignal(1, active=0, async=True)
    tick = Signal(intbv(0, min=0, max=1))
    inc_inst = toVHDL(GenTicks, clock, reset, tick, 50)