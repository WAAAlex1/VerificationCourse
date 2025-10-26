#
# Simple random cocotb test using random library.
#

import cocotb
import random

from cocotb.triggers import RisingEdge, ClockCycles, ReadOnly
from cocotb.clock import Clock

@cocotb.test()
async def sat_random_test(dut):
    """ Test sends 10 random inputs."""

    # Create a 2ns period clock on port clk
    clock = Clock(dut.clk, 2.5, units="ns")

    # Start the clock
    cocotb.start_soon(clock.start())

    dut.rst.value = 0
    dut.in_data.value = 0
    dut.in_valid.value = 0

    await RisingEdge(dut.clk)

    dut.rst.value = 1

    await RisingEdge(dut.clk)

    dut.rst.value = 0

    await RisingEdge(dut.clk)

    for i in range(10):

        # Random inputs
        in_data = random.randint(0, 15)

        # Drive input ports
        dut.in_data.value = in_data
        dut.in_valid.value = 1

        # Wait for CLK to let RTL update state
        await RisingEdge(dut.clk)