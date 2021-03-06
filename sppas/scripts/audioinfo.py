#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /        Automatic
#           \__   |__/  |__/  |___| \__      Annotation
#              \  |     |     |   |    \     of
#           ___/  |     |     |   | ___/     Speech
#           =============================
#
#           http://www.lpl-aix.fr/~bigi/sppas
#
# ---------------------------------------------------------------------------
# developed at:
#
#       Laboratoire Parole et Langage
#
#       Copyright (C) 2011-2014  Brigitte Bigi
#
#       Use of this software is governed by the GPL, v3
#       This banner notice must not be removed
# ---------------------------------------------------------------------------
#
# SPPAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPPAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPPAS. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------
# File: audioinfo.py
# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors___  = """Brigitte Bigi (brigitte.bigi@gmail.com)"""
__copyright__ = """Copyright (C) 2011-2014  Brigitte Bigi"""

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

import sys
import os
import os.path
from argparse import ArgumentParser

PROGRAM = os.path.abspath(__file__)
SPPAS = os.path.join(os.path.dirname( os.path.dirname( PROGRAM ) ), "src")
sys.path.append(SPPAS)

import audiodata.aio
from audiodata.audiovolume   import AudioVolume
from audiodata.channelvolume import ChannelVolume
from audiodata.audioframes   import AudioFrames

# ----------------------------------------------------------------------------
# Verify and extract args:
# ----------------------------------------------------------------------------

parser = ArgumentParser(usage="%s -w file [options]" % os.path.basename(PROGRAM), description="... a script to get information about an audio file.")

parser.add_argument("-w", metavar="file", required=True,  help='Input audio file name')
parser.add_argument("-f", metavar="value", default=0.01, type=float, help='Frame duration to estimate rms values (default: 0.01)')

if len(sys.argv) <= 1:
    sys.argv.append('-h')

args = parser.parse_args()

# ----------------------------------------------------------------------------

audio = audiodata.aio.open(args.w)
audio.frameduration = args.f

print "Audio file name:     ", args.w
print "Duration (seconds):  ", audio.get_duration()
print "Frame rate (Hz):     ", audio.get_framerate()
print "Sample width (bits): ", audio.get_sampwidth()*8
nc = audio.get_nchannels()
print "Number of channels:  ", nc

if nc == 1:
    print "Clipping rate (in %):"
    for i in range(2,9,2):
        f = float(i)/10.
        c = audio.clipping_rate( f ) * 100.
        print "  - factor=%.1f:      %.3f"%(f,c)

    audiovol = AudioVolume(audio, args.f)
    print "Volume:"
    print "  - min:           ", audiovol.min()
    print "  - max:           ", audiovol.max()
    print "  - mean:          ", round(audiovol.mean(),2)
    print "  - median:        ", round(audiovol.median(),2)
    print "  - stdev:         ", round(audiovol.stdev(),2)
    print "  - coefvariation: ", round(audiovol.coefvariation(),2)

else:

    for n in range(nc):
        print "Channel %d:"%(n)
        cidx = audio.extract_channel(n)
        channel = audio.get_channel(cidx)

        # Values related to amplitude
        frames = channel.get_frames(channel.get_nframes())
        ca = AudioFrames(frames, channel.get_sampwidth(), 1)
        for i in range(2,9,2):
            f = float(i)/10.
            c = ca.clipping_rate( f ) * 100.
            print "  - factor=%.1f:      %.3f"%(f,c)

        # RMS (=volume)
        cv = ChannelVolume( channel )
        print "  Volume:"
        print "    - min:           ", cv.min()
        print "    - max:           ", cv.max()
        print "    - mean:          ", round(cv.mean(),2)
        print "    - median:        ", round(cv.median(),2)
        print "    - stdev:         ", round(cv.stdev(),2)
        print "    - coefvariation: ", round(cv.coefvariation(),2)

# ----------------------------------------------------------------------------
