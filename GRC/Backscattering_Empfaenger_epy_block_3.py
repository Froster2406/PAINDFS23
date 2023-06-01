import sys
import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, corr_length=4096):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Correlation',   # will show up in GRC
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64]
        )
        
        # self.logg = gr.logger()
        self.corr_length = corr_length
        
        np.set_printoptions(threshold=sys.maxsize)
        self.buf = np.array([[], []])
        self.buf_out = np.array(np.zeros(self.corr_length))
        
    def work(self, input_items, output_items):
        self.buf = np.concatenate((self.buf, input_items), axis=1)
        
        tmp = np.array([])
        out_len = np.array(output_items).shape[1]
        
        #print("out len " + str(out_len))
        
        while self.buf.shape[1] >= self.corr_length:
                tmp = self.buf[:, :self.corr_length]
                self.buf = self.buf[:, self.corr_length:]
                
                corr = np.flip(np.correlate(tmp[0], tmp[1], 'full')[:self.corr_length])
                self.buf_out = np.concatenate((self.buf_out, corr))
        
        output_items[0][:] = self.buf_out[:out_len]
        self.buf_out = self.buf_out[out_len:]
        
        # print("tmp " + str(tmp.shape))
        # print("out " + str(np.array(output_items).shape))
        
        return len(output_items[0])
