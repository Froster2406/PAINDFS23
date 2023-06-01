"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Deinterleaving',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.array1 = []
        self.array2 = []
        self.array3 = []
        self.array4 = []
        self.array5 = []
        self.array6 = []
        self.array7 = []
        self.array8 = []
        self.counter = 0

    def work(self, input_items, output_items):
        self.array1[self.counter] = (self.array1[self.counter] | input_items[0].real)
        self.array2[self.counter] = (self.array2[self.counter] | input_items[0].real)
        self.array3[self.counter] = (self.array3[self.counter] | input_items[0].real)
        self.array4[self.counter] = (self.array4[self.counter] | input_items[0].real)
        self.array5[self.counter] = (self.array5[self.counter] | input_items[0].real)
        self.array6[self.counter] = (self.array6[self.counter] | input_items[0].real)
        self.array7[self.counter] = (self.array7[self.counter] | input_items[0].real)
        self.array8[self.counter] = (self.array8[self.counter] | input_items[0].real)
        self.counter = self.counter + 1
        if self.counter == 8:
            output_items[0][:] = self.array1
            output_items[0][:] = self.array2
            output_items[0][:] = self.array3
            output_items[0][:] = self.array4
            output_items[0][:] = self.array5
            output_items[0][:] = self.array6
            output_items[0][:] = self.array7
            output_items[0][:] = self.array8
            self.array1 = []
            self.array2 = []
            self.array3 = []
            self.array4 = []
            self.array5 = []
            self.array6 = []
            self.array7 = []
            self.array8 = []
            self.counter = 0
