#
# Simple random cocotb test using random library.
#

import cocotb
import vsc

from cocotb.triggers import RisingEdge, ClockCycles, ReadOnly
from cocotb.clock import Clock
from cocotb.binary import BinaryValue

from utilities import create_coverage_report
from sat_filter_coverage import covergroup_ssdt

import warnings
# Quick fix because of warnings of PyVSC
warnings.simplefilter("ignore")

@vsc.randobj
class input:
    def __init__(self):
        self.in_data = vsc.rand_bit_t(4)
        self.nbr_itr = vsc.rand_uint8_t()

    @vsc.constraint
    def in_data_constraint(self):
        self.in_data >= 0
        self.in_data <= 15

    @vsc.constraint
    def nbr_itr_constraint(self):
        self.nbr_itr > 0
        self.nbr_itr < 100

@cocotb.test()
async def sat_random_test(dut):
    """ Test sends x random inputs."""

    # Create a 2ns period clock on port clk
    clock = Clock(dut.clk, 2.5, units="ns")

    # Start the clock
    cocotb.start_soon(clock.start())

    # Implement coverage agent
    coverage = covergroup_ssdt()

    # Instantiate random input class
    rand_inputs = input()

    # Randomize once for random number of iterations
    rand_inputs.randomize()
    nbr_itr = rand_inputs.nbr_itr
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
    dut.in_valid.value = 1

    # Generate random data and apply it
    for i in range(nbr_itr): # Restricted to only 10 runs due to this exercise. Otherwise, use nbr_itr

        # Random inputs
        rand_inputs.randomize()
        print(f"Generated Random Data input: {rand_inputs.in_data} | sequence number {i}")

        # Drive input ports
        dut.in_data.value = rand_inputs.in_data

        # Wait for CLK to let RTL update state
        await ClockCycles(dut.clk, 1)

        if dut.out_valid.value == 1:
            coverage.sample(dut.out_data.value)

    # Reset input values
    dut.in_data.value = 0
    dut.in_valid.value = 0

    await ClockCycles(dut.clk, 2)

    create_coverage_report("sat_random_test_pyvsc_rnd")