# Simple tests for an adder module
import random

import cocotb
from cocotb.triggers import RisingEdge, ClockCycles, Timer, ReadOnly
from cocotb.clock import Clock

from mux_model import mux_model


@cocotb.test()
async def mux_basic_test(dut):
    """Simple test case"""

    clk = Clock(signal=dut.clk, period=2, units="ns")
    cocotb.start(clk.start())

    A = 0b0001
    Sel = 0

    dut.A.value = A
    dut.sel.value = Sel

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.out.value == mux_model(
        A, Sel
    ), f"Mux result is incorrect: {dut.out.value} != 1"


@cocotb.test()
async def mux_randomised_test(dut):
    """Test for selecting randomized values"""

    clk = Clock(signal=dut.clk, period=2, units="ns")
    cocotb.start(clk.start())

    dut.A.value = 0
    dut.sel.value = 0

    await RisingEdge(dut.clk)

    for i in range(10):
        # Random inputs
        A = random.randint(0, 15)
        Sel = random.randint(0, 3)

        # Drive input ports
        dut.A.value = A
        dut.sel.value = Sel

        # Wait for CLK to let RTL update state
        await RisingEdge(dut.clk)

        # Wait for delta cycles to settle
        await ReadOnly()

        expected_result = mux_model(A, Sel)

        # Wait for output to be put on output port
        await RisingEdge(dut.clk)

        assert dut.out.value == expected_result, f"Randomised test failed with - Input: {dut.A.value}, Select: {dut.sel.value}, Result: {dut.out.value}"
