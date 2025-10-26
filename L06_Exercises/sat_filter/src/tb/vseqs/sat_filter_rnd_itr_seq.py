import cocotb
import vsc
from cocotb.triggers import Combine

from sat_filter_tb_base_seq import sat_filter_tb_base_seq
from uvc.ssdt.src.uvc_ssdt_sequence_lib import uvc_ssdt_default_seq

# User input value (threshold for max sequences)
_MAX_CNSTRNT = 100

@vsc.randobj
class sat_filter_rnd_itr_seq(sat_filter_tb_base_seq):
    """ Random sequence for the Saturation Filter TB. """

    def __init__(self, name="sat_filter_rnd_itr_seq"):
        super().__init__(name)

        self.producer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_prod_seq")
        self.consumer_seq = uvc_ssdt_default_seq.create("sat_filter_ssdt_cons_seq")

        self.itr_nbr = vsc.rand_uint8_t()

    async def body(self):

        # Launch sequences
        await super().body()

        seq_cnt = 0;

        # Call coroutines
        for i in range(self.itr_nbr):
            prod_task = cocotb.start_soon(self.producer_seq.start(self.sequencer.ssdt_producer_sequencer))
            cons_task = cocotb.start_soon(self.consumer_seq.start(self.sequencer.ssdt_consumer_sequencer))

            # Finishes when the both tasks finishes
            await Combine(prod_task, cons_task)

            seq_cnt += 1;

        print(f"Number of sequences ran: {seq_cnt}")


    @vsc.constraint
    def cnstrnt(self):
        self.itr_nbr >= 0
        self.itr_nbr < _MAX_CNSTRNT
