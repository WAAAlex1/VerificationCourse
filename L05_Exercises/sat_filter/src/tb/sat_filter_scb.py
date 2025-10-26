

""" Saturation Filter Scoreboard
- Verification component that contains checkers and verifies the functionality of the design.
- Receives transaction level objects captured from the interfaces of a DUT via TLM Analysis Ports.
- Includes the Reference Model.
"""

import cocotb
from pyuvm import uvm_scoreboard, uvm_analysis_port, uvm_tlm_analysis_fifo, ConfigDB
from cocotb.queue import Queue

class sat_filter_scoreboard(uvm_scoreboard):
    """ Scoreboard for Saturation Filter. """

    def __init__(self, name="sat_filter_scoreboard", parent=None):

        super().__init__(name, parent)

        # Declaration of components
        self.cfg = None

        self.analysis_port = None   # Analysis Port handler

        # FIFO for connecting to UVC's ap
        self.uvc_ssdt_consumer_fifo = None
        self.ref_model_fifo = None

        # recording number of successes and failures
        self.succes = 0
        self.failure = 0

    def build_phase(self):

        super().build_phase()

        # Get the configuration object
        self.cfg = ConfigDB().get(self, "", "cfg")
        self.logger.debug(f" Config of < {self.get_name()} > is {(self.cfg.__getattribute__)}")

        # Instantiate the analysis port
        self.analysis_port = uvm_analysis_port(f"{self.get_name()}_analysis_port", self)

        # Create the analysis FIFOs
        self.uvc_ssdt_consumer_fifo = uvm_tlm_analysis_fifo("uvc_ssdt_consumer_fifo", self)
        self.ref_model_fifo = uvm_tlm_analysis_fifo("ref_model_fifo", self)

        # Queues to store output of Ref. Model
        self.uvc_ssdt_consumer_queue = Queue(maxsize=1)
        self.ref_model_queue = Queue(maxsize=1)

    async def run_phase(self):

        await super().run_phase()

        while True:
            await self.transfer_item()
            await self.compare_items()

    # Report the results of the comparisons
    def check_phase(self):

        super().check_phase()

        self.logger.info(f"Number of total transcations: {self.succes + self.failure}")
        self.logger.info(f"Number of successfull transactions: {self.succes}")
        self.logger.info(f"Number of erroneous transactions: {self.failure}")

    async def transfer_item(self):

        fifo_consumer_item = await self.uvc_ssdt_consumer_fifo.get()
        fifo_ref_item = await self.ref_model_fifo.get()

        await self.uvc_ssdt_consumer_queue.put(fifo_consumer_item)
        await self.ref_model_queue.put(fifo_ref_item)

    async def compare_items(self):

        consumer_val = await self.uvc_ssdt_consumer_queue.get()
        ref_val = await self.ref_model_queue.get()

        if consumer_val == ref_val:
            self.succes += 1
        else:
            self.logger.info(f"ERROR!!!! Expected value {ref_val} Different from actual value {consumer_val}")
            self.failure += 1
