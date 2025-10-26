#
# Simple random cocotb test using random library.
#

import cocotb
import random
import vsc

from cocotb.triggers import RisingEdge, ClockCycles, ReadOnly
from cocotb.clock import Clock


@vsc.randobj
class input:
    def __init__(self):
        self.in_data = vsc.rand_bit_t(4)
        self.nbr_itr = vsc.rand_uint8_t()

    @vsc.constraint
    def in_data_constraint(self):
        self.in_data > 0
        self.in_data < 14

    @vsc.constraint
    def nbr_itr_constraint(self):
        self.nbr_itr > 0
        self.nbr_itr < 100

@cocotb.test()
async def sat_random_test(dut):
    """ Test sends 10 random inputs."""

    # Create a 2ns period clock on port clk
    clock = Clock(dut.clk, 2.5, units="ns")

    # Start the clock
    cocotb.start_soon(clock.start())

    # Instantiate random input class
    inputs = input()

    # Randomize once for random number of iterations
    inputs.randomize()
    nbr_itr = inputs.nbr_itr
    print(f"Number of iterations: {nbr_itr} ")

    # Standard values
    dut.rst.value = 0
    dut.in_data.value = 0
    dut.in_valid.value = 0

    # Standard reset procedure to start
    await RisingEdge(dut.clk)
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Generate random data and apply it
    for i in range(nbr_itr):

        # Random inputs
        inputs.randomize()
        print(f"Generated Random Data input: {inputs.in_data} | sequence number {i}")

        # Drive input ports
        dut.in_data.value = inputs.in_data

        # Wait for CLK to let RTL update state
        await RisingEdge(dut.clk)

