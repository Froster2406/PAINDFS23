#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Backscattering - Receiver
# Author: Stefano Nicora
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import Backscattering_Empfaenger_epy_block_0_0 as epy_block_0_0  # embedded python block
import Backscattering_Empfaenger_epy_block_0_1_0 as epy_block_0_1_0  # embedded python block
import Backscattering_Empfaenger_epy_block_0_1_1 as epy_block_0_1_1  # embedded python block



from gnuradio import qtgui

class Backscattering_Empfaenger(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Backscattering - Receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Backscattering - Receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Backscattering_Empfaenger")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10 #2e6
        self.chooser = chooser = 2422000000
        self.bit_time_length = bit_time_length = 10
        self.RX_gain = RX_gain = 10

        ##################################################
        # Blocks
        ##################################################

        self.epy_block_0_1_1 = epy_block_0_1_1.blk()
        self.epy_block_0_1_0 = epy_block_0_1_0.blk()
        self.epy_block_0_0 = epy_block_0_0.blk()
        # Create the options list
        self._chooser_options = [2412000000.0, 2417000000.0, 2422000000.0, 2427000000.0, 2432000000.0, 2437000000.0, 2442000000.0, 2447000000.0, 2452000000.0, 2457000000.0, 2462000000.0, 2467000000.0, 2472000000.0]
        # Create the labels list
        self._chooser_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        # Create the combo box
        # Create the radio buttons
        self._chooser_group_box = Qt.QGroupBox("'chooser'" + ": ")
        self._chooser_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._chooser_button_group = variable_chooser_button_group()
        self._chooser_group_box.setLayout(self._chooser_box)
        for i, _label in enumerate(self._chooser_labels):
            radio_button = Qt.QRadioButton(_label)
            self._chooser_box.addWidget(radio_button)
            self._chooser_button_group.addButton(radio_button, i)
        self._chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chooser_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._chooser_options.index(i)))
        self._chooser_callback(self.chooser)
        self._chooser_button_group.buttonClicked[int].connect(
            lambda i: self.set_chooser(self._chooser_options[i]))
        self.top_layout.addWidget(self._chooser_group_box)
        self.blocks_vector_source_x_0_0_0_0_0_0 = blocks.vector_source_c((1,1,1,0,0,0,1,0,0,1,0), True, 1, [])
        self._RX_gain_range = Range(0, 60, 1, 10, 200)
        self._RX_gain_win = RangeWidget(self._RX_gain_range, self.set_RX_gain, "RX Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._RX_gain_win)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0_0_0_0_0_0, 0), (self.epy_block_0_1_0, 0))
        self.connect((self.blocks_vector_source_x_0_0_0_0_0_0, 0), (self.epy_block_0_1_0, 1))
        self.connect((self.epy_block_0_0, 0), (self.epy_block_0_1_1, 0))
        self.connect((self.epy_block_0_1_0, 0), (self.epy_block_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Backscattering_Empfaenger")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_chooser(self):
        return self.chooser

    def set_chooser(self, chooser):
        self.chooser = chooser
        self._chooser_callback(self.chooser)

    def get_bit_time_length(self):
        return self.bit_time_length

    def set_bit_time_length(self, bit_time_length):
        self.bit_time_length = bit_time_length

    def get_RX_gain(self):
        return self.RX_gain

    def set_RX_gain(self, RX_gain):
        self.RX_gain = RX_gain




def main(top_block_cls=Backscattering_Empfaenger, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
