#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AM Modulation With Frequency estimation
# Author: Caio Rodrigues e Leonardo Pessôa
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import math
import sip



class AM_Implementation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AM Modulation With Frequency estimation", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AM Modulation With Frequency estimation")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "AM_Implementation")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.noise = noise = 0
        self.loopF = loopF = 0.03
        self.SPS = SPS = 32
        self.LPrec = LPrec = 1
        self.FreqOffset = FreqOffset = 0
        self.AM = AM = digital.constellation_calcdist([0,1,2,3], [0,1,2,3],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.AM.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        self._noise_range = qtgui.Range(0, 1, 0.01, 0, 200)
        self._noise_win = qtgui.RangeWidget(self._noise_range, self.set_noise, "noise", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._noise_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._loopF_range = qtgui.Range(0.001, 0.1, 0.001, 0.03, 200)
        self._loopF_win = qtgui.RangeWidget(self._loopF_range, self.set_loopF, "Loop Filter PLL", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._loopF_win)
        self._LPrec_range = qtgui.Range(0.2, 2, 0.05, 1, 200)
        self._LPrec_win = qtgui.RangeWidget(self._LPrec_range, self.set_LPrec, "Low Pass receptor Filter", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._LPrec_win)
        self._FreqOffset_range = qtgui.Range(-100, 100, 1, 0, 200)
        self._FreqOffset_win = qtgui.RangeWidget(self._FreqOffset_range, self.set_FreqOffset, "Carrier Freq Offset", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._FreqOffset_win, 5, 0, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_1 = qtgui.time_sink_f(
            (int(1024*8)), #size
            samp_rate, #samp_rate
            'Sinal mensagem', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_1.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_1_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0_1_0 = qtgui.time_sink_f(
            (int(1024*8)), #size
            samp_rate, #samp_rate
            'Channel Signal', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0_1_0.set_y_axis(4150, 3850)

        self.qtgui_time_sink_x_0_0_0_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_1_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_1_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_1_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_0_1_0_win)
        self.qtgui_time_sink_x_0_0_0_0 = qtgui.time_sink_f(
            (int(1024*8)), #size
            samp_rate, #samp_rate
            'Receptor Signal', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_0_0_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_2_0_0_0_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Receptor Signal (original)', #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_2_0_0_0_1.set_update_time(0.1)
        self.qtgui_freq_sink_x_2_0_0_0_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_2_0_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2_0_0_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_2_0_0_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_2_0_0_0_1.set_fft_average(0.1)
        self.qtgui_freq_sink_x_2_0_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2_0_0_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_2_0_0_0_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_2_0_0_0_1.set_plot_pos_half(not True)

        labels = ['Pre-Filtro', 'Pós-Filtro', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_0_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_2_0_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_2_0_0_0_1_win)
        self.qtgui_freq_sink_x_2_0_0_0_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'VCO', #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_2_0_0_0_0.set_update_time(0.1)
        self.qtgui_freq_sink_x_2_0_0_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_2_0_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2_0_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_2_0_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_2_0_0_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_2_0_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2_0_0_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_2_0_0_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_2_0_0_0_0.set_plot_pos_half(not True)

        labels = ['Sinal de saída do VCO', 'Sinal de referência', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_0_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_2_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_2_0_0_0_0_win)
        self.qtgui_freq_sink_x_2_0_0_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'Receptor Signal pre filtro', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_2_0_0_0.set_update_time(0.1)
        self.qtgui_freq_sink_x_2_0_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_2_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_2_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_2_0_0_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_2_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2_0_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_2_0_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_2_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_2_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_2_0_0_0_win)
        self.low_pass_filter_0_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (1.2*samp_rate//SPS),
                1,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (LPrec*samp_rate//SPS),
                1,
                window.WIN_HAMMING,
                0.1))
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=AM,
            differential=True,
            samples_per_symbol=SPS,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_vco_f_0 = blocks.vco_f(samp_rate, ((2*math.pi)), 1)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(((samp_rate)/(2*math.pi)))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, (4*samp_rate//SPS), 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, (4*samp_rate//SPS + FreqOffset), 1, 0, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 4, 1000))), True)
        self.analog_pll_freqdet_cf_1 = analog.pll_freqdet_cf((loopF*math.pi/100), (2* math.pi * (4*samp_rate//SPS + 100) / samp_rate), (2* math.pi * (4*samp_rate//SPS - 100) / samp_rate))
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, noise, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_pll_freqdet_cf_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.qtgui_freq_sink_x_2_0_0_0_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_0_0_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.analog_pll_freqdet_cf_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_vco_f_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0_0_0_1_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.qtgui_freq_sink_x_2_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.qtgui_freq_sink_x_2_0_0_0_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_vco_f_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_vco_f_0, 0), (self.qtgui_freq_sink_x_2_0_0_0_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_time_sink_x_0_0_0_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.qtgui_freq_sink_x_2_0_0_0_1, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AM_Implementation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_pll_freqdet_cf_1.set_max_freq((2* math.pi * (4*self.samp_rate//self.SPS + 100) / self.samp_rate))
        self.analog_pll_freqdet_cf_1.set_min_freq((2* math.pi * (4*self.samp_rate//self.SPS - 100) / self.samp_rate))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_frequency((4*self.samp_rate//self.SPS + self.FreqOffset))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_frequency((4*self.samp_rate//self.SPS))
        self.blocks_multiply_const_vxx_0.set_k(((self.samp_rate)/(2*math.pi)))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.LPrec*self.samp_rate//self.SPS), 1, window.WIN_HAMMING, 0.1))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.samp_rate, (1.2*self.samp_rate//self.SPS), 1, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_2_0_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_2_0_0_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_2_0_0_0_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0_1_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_1.set_samp_rate(self.samp_rate)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.analog_noise_source_x_0.set_amplitude(self.noise)

    def get_loopF(self):
        return self.loopF

    def set_loopF(self, loopF):
        self.loopF = loopF
        self.analog_pll_freqdet_cf_1.set_loop_bandwidth((self.loopF*math.pi/100))

    def get_SPS(self):
        return self.SPS

    def set_SPS(self, SPS):
        self.SPS = SPS
        self.analog_pll_freqdet_cf_1.set_max_freq((2* math.pi * (4*self.samp_rate//self.SPS + 100) / self.samp_rate))
        self.analog_pll_freqdet_cf_1.set_min_freq((2* math.pi * (4*self.samp_rate//self.SPS - 100) / self.samp_rate))
        self.analog_sig_source_x_0.set_frequency((4*self.samp_rate//self.SPS + self.FreqOffset))
        self.analog_sig_source_x_0_0.set_frequency((4*self.samp_rate//self.SPS))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.LPrec*self.samp_rate//self.SPS), 1, window.WIN_HAMMING, 0.1))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.samp_rate, (1.2*self.samp_rate//self.SPS), 1, window.WIN_HAMMING, 6.76))

    def get_LPrec(self):
        return self.LPrec

    def set_LPrec(self, LPrec):
        self.LPrec = LPrec
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.LPrec*self.samp_rate//self.SPS), 1, window.WIN_HAMMING, 0.1))

    def get_FreqOffset(self):
        return self.FreqOffset

    def set_FreqOffset(self, FreqOffset):
        self.FreqOffset = FreqOffset
        self.analog_sig_source_x_0.set_frequency((4*self.samp_rate//self.SPS + self.FreqOffset))

    def get_AM(self):
        return self.AM

    def set_AM(self, AM):
        self.AM = AM




def main(top_block_cls=AM_Implementation, options=None):

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
