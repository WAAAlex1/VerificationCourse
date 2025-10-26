
import vsc
from vsc import bit_t

@vsc.covergroup
class covergroup_ssdt(object):

    def __init__(self):

        self.with_sample(
            out_data=bit_t(4)
        )

        MAX_VALUE = (2 ** 4)

        self.cp1 = vsc.coverpoint(self.out_data, bins={
            "min": vsc.bin(0),
            "range": vsc.bin([1, 14]),
            "max": vsc.bin(15)
        })

