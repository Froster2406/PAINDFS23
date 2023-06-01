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
			name='Hamming',
			in_sig=[np.complex64,np.complex64],
			out_sig=[np.complex64]
		)
	def work(self, input_items, output_items):
		if input_items[1].real > 10:
			# revert hamming-encoding if preamble value is large enough
			colum2or4 = 1
			colum3or4 = 1
			row2or4 = 1
			row3or4 = 1
			generalBitflip = 1
			faultyBit = 0
			# check if all parity bits are correct | 1 = flip occurred
			if (input_items[0][1].real ^ input_items[0][2].real ^ input_items[0][3].real ^ input_items[0][4].real ^ input_items[0][5].real ^ input_items[0][6].real ^ input_items[0][7].real ^ input_items[0][8].real ^ input_items[0][9].real ^ input_items[0][10].real ^ input_items[0][11].real ^ input_items[0][12].real ^ input_items[0][13].real ^ input_items[0][14].real ^ input_items[0][15].real & 1) == 0:
				generalBitflip = 0
			if generalBitflip == 1:
				print("There has been at least a second bit flip that couldn't be processed. Aborting...")
				quit()
			if (input_items[0][1].real ^ input_items[0][3].real ^ input_items[0][5].real ^ input_items[0][7].real ^ input_items[0][9].real ^ input_items[0][11].real ^ input_items[0][13].real ^ input_items[0][15].real & 1) == 0:
				colum2or4 = 0
			if (input_items[0][2].real ^ input_items[0][3].real ^ input_items[0][6].real ^ input_items[0][7].real ^ input_items[0][10].real ^ input_items[0][11].real ^ input_items[0][14].real ^ input_items[0][15].real & 1) == 0:
				colum3or4 = 0
			if (input_items[0][4].real ^ input_items[0][5].real ^ input_items[0][6].real ^ input_items[0][7].real ^ input_items[0][12].real ^ input_items[0][13].real ^ input_items[0][14].real ^ input_items[0][15].real & 1) == 0:
				row2or4 = 0
			if (input_items[0][8].real ^ input_items[0][9].real ^ input_items[0][10].real ^ input_items[0][11].real ^ input_items[0][12].real ^ input_items[0][13].real ^ input_items[0][14].real ^ input_items[0][15].real & 1) == 0:
				row3or4 = 0
			faultyBit = (row3or4 << 3) | (row2or4 << 2) | (colum3or4 << 1) | colum2or4 # calculate position of faulty / flipped bit
			if faultyBit != 0:	# switch wrong bit
				input_items[0][faultyBit] = input_items[0][faultyBit] ^ 1
			output_items[0][:] = input_items[0]
		return len(output_items[0])