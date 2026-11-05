#!/usr/bin/env python

from GPMsDB_tk.common import PeakLoader
__author__ = 'Yuji Sekiguchi'
__copyright__ = ('Copyright (c) 2022 Yuji Sekiguchi, National Institute of Advanced Industrial Science and Technology (AIST); '
                 'Copyright (C) 2026 Manuel Escalera (modifications)')
__credits__ = ['Yuji Sekiguchi']
__license__ = 'GPL3.0'
__maintainer__ = 'Yuji Sekiguchi'
__email__ = 'y.sekiguchi@aist.go.jp'
__status__ = 'Development'

import os
import sys
import logging
import warnings

logging.getLogger('matplotlib.fontmanager').setLevel(logging.ERROR)
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib.font_manager')

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.rcParams.update({'figure.max_open_warning': 0})


class PlotPeaks(object):
    def __init__(self):
        self.figdpi = 200
        self.minimum = 0
        self.logger = logging.getLogger('GPMsDB_tk')

    def run(self, input_list, out_dir, filetype):
        if filetype.lower() == "pdf":
            figdpi = 72
        else:
            figdpi = self.figdpi

        basename = os.path.basename(input_list)
        basename_without_ext = os.path.splitext(
            os.path.basename(input_list))[0]
        outfile = os.path.join(
            out_dir, basename_without_ext + "_inspect." + filetype)

        intens, t, tp, com = PeakLoader(input_list, self.minimum)
        if len(list(intens)) == 0:
            self.logger.error("No peaks found")
            sys.exit(1)

        if com == "":
            com = "not specified"

        peaks0, peaks1, peaks2, peaks3, peaks4, peaks5 = {}, {}, {}, {}, {}, {}

        for x in intens:
            if float(intens[x]) > 0.01:
                peaks0[x] = intens[x]
            elif 0.005 < float(intens[x]) <= 0.01:
                peaks1[x] = intens[x]
            elif 0.002 < float(intens[x]) <= 0.005:
                peaks2[x] = intens[x]
            elif 0.0005 < float(intens[x]) <= 0.002:
                peaks3[x] = intens[x]
            elif 0.0001 < float(intens[x]) <= 0.0005:
                peaks4[x] = intens[x]
            elif float(intens[x]) <= 0.0001:
                peaks5[x] = intens[x]

        l1 = 0.01
        l2 = 0.005
        l3 = 0.002
        l4 = 0.0005
        l5 = 0.0001

        x = list(peaks0.keys())
        y = list(peaks0.values())
        x1 = list(peaks1.keys())
        y1 = list(peaks1.values())
        x2 = list(peaks2.keys())
        y2 = list(peaks2.values())
        x3 = list(peaks3.keys())
        y3 = list(peaks3.values())
        x4 = list(peaks4.keys())
        y4 = list(peaks4.values())
        x5 = list(peaks5.keys())
        y5 = list(peaks5.values())
        title = str("Peak list information for " + str(basename) + "\n" +
                    "Total number of peaks: " + str(len(intens)) + ",  " +
                    "COM=" + com + "\n" +
                    "Relative intensity >1%, " + str(len(peaks0)) + " peaks; "
                    "1-0.5%, " + str(len(peaks1)) + " peaks; " +
                    "0.5-0.2%, " + str(len(peaks2)) + " peaks; " +
                    "0.2-0.05%, " + str(len(peaks3)) + " peaks; " +
                    "0.05-0.01%, " + str(len(peaks4)) + " peaks; " +
                    "<0.01%, " + str(len(peaks5)) + " peaks\n" +
                    "Black plots: higer than 1%, blue: 1-0.5%, orange: 0.5-0.2%, green: 0.2-0.05, red: 0.05-0.01%, purple: < 0.01%")

        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans','Liberation Sans']
        plt.rcParams["font.size"] = 12
        
        fm._load_fontmanager(try_read_cache =False)

        fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(15,10))
        fig.patch.set_facecolor('white')
        fig.suptitle(title, fontsize=12, x=fig.subplotpars.left, ha='left')

        if not len(peaks0) == 0:
            ax1.stem(x, y, linefmt="k-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks1) == 0:
            ax1.stem(x1, y1, linefmt="C0-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks2) == 0:
            ax1.stem(x2, y2, linefmt="C1-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks3) == 0:
            ax1.stem(x3, y3, linefmt="C2-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks4) == 0:
            ax1.stem(x4, y4, linefmt="C3-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks5) == 0:
            ax1.stem(x5, y5, linefmt="C4-", basefmt=" ",
                     markerfmt=" ")

        ax1.hlines(l1, 0, 20000, 'C0', linestyles='dashed', lw=0.5)
        ax1.text(50, l1, "1% line", size=10, color='C0')
        ax1.hlines(l2, 0, 20000, 'C1', linestyles='dashed', lw=0.5)
        ax1.text(50, l2, "0.5% line", size=10, color='C1')
        ax1.hlines(l3, 0, 20000, 'C2', linestyles='dashed', lw=0.5)
        ax1.text(50, l3, "0.2% line", size=10, color='C2')
        ax1.hlines(l4, 0, 20000, 'C3', linestyles='dashed', lw=0.5)
        ax1.text(50, l4, "0.05% line", size=10, color='C4')
        ax1.hlines(l5, 0, 20000, 'C3', linestyles='dashed', lw=0.5)
        ax1.text(50, l5, "0.01% line", size=10, color='C4')

        ax1.grid(True, axis="y", color='black', linestyle=':', linewidth=0.5)
        ax1.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, loc: "{:,}".format(int(x))))
        ax1.set_ylim(0,)
        ax1.set_xlim(0, 15000)
        ax1.set_xlabel("m/z", fontsize=14)
        ax1.set_ylabel("intensity (linear, -)", fontsize=14)

        ax2.set_yscale('log')

        if not len(peaks0) == 0:
            ax2.stem(x, y, linefmt="k-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks1) == 0:
            ax2.stem(x1, y1, linefmt="C0-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks2) == 0:
            ax2.stem(x2, y2, linefmt="C1-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks3) == 0:
            ax2.stem(x3, y3, linefmt="C2-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks4) == 0:
            ax2.stem(x4, y4, linefmt="C3-", basefmt=" ",
                     markerfmt=" ")
        if not len(peaks5) == 0:
            ax2.stem(x5, y5, linefmt="C4-", basefmt=" ",
                     markerfmt=" ")

        ax2.hlines(l1, 0, 20000, 'C0', linestyles='dashed', lw=0.5)
        ax2.text(50, l1, "1% line", size=10, color='C0')
        ax2.hlines(l2, 0, 20000, 'C1', linestyles='dashed', lw=0.5)
        ax2.text(50, l2, "0.5% line", size=10, color='C1')
        ax2.hlines(l3, 0, 20000, 'C2', linestyles='dashed', lw=0.5)
        ax2.text(50, l3, "0.2% line", size=10, color='C2')
        ax2.hlines(l4, 0, 20000, 'C3', linestyles='dashed', lw=0.5)
        ax2.text(50, l4, "0.05% line", size=10, color='C3')
        ax2.hlines(l5, 0, 20000, 'C4', linestyles='dashed', lw=0.5)
        ax2.text(50, l5, "0.01% line", size=10, color='C4')

        ax2.grid(True, axis="y", color='black', linestyle=':', linewidth=0.5)
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, loc: "{:,}".format(int(x))))
        ax2.set_xlim(0, 15000)
        ax2.set_xlabel("m/z", fontsize=14)
        ax2.set_ylabel("intensity (log, -)", fontsize=14)

        plt.savefig(outfile, dpi=figdpi, format=filetype,
                    bbox_inches='tight', pad_inches=0.1)
        plt.close()

        return outfile
