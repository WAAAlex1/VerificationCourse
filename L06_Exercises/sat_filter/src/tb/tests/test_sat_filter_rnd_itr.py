import cocotb
import pyuvm

from pyuvm import uvm_factory

from sat_filter_tb_base_test import sat_filter_tb_base_test
from sat_filter_tb_base_seq import sat_filter_tb_base_seq

from vseqs.sat_filter_default_seq import sat_filter_default_seq
from vseqs.sat_filter_rnd_itr_seq import sat_filter_rnd_itr_seq

# Default values
_TIMEOUT_TIME = 1000
_TIMEOUT_UNIT = 'ns'

@pyuvm.test(timeout_time=_TIMEOUT_TIME, timeout_unit=_TIMEOUT_UNIT)
class test_sat_filter_rnd_itr(sat_filter_tb_base_test):
    def __init__(self, name="test_sat_filter_rnd_itr", parent = None):
        super().__init__(name, parent)

    def start_of_simulation_phase(self):
        super().start_of_simulation_phase()

        uvm_factory().set_type_override_by_type(sat_filter_tb_base_seq, sat_filter_rnd_itr_seq)

    async def run_phase(self):

        self.raise_objection()
        await super().run_phase()

        # Randomize sequence (inline)
        with self.virt_sequence.randomize_with() as it:
            it.itr_nbr >= 10

        print(f"Random number of sequences generated: {self.virt_sequence.itr_nbr}")

        # Run sequence
        await self.virt_sequence.start(self.tb_env.virtual_sequencer)

        self.drop_objection()

