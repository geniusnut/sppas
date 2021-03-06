#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /              Automatic
#           \__   |__/  |__/  |___| \__             Annotation
#              \  |     |     |   |    \             of
#           ___/  |     |     |   | ___/              Speech
#
#
#                           http://www.sppas.org/
#
# ---------------------------------------------------------------------------
#            Laboratoire Parole et Langage, Aix-en-Provence, France
#                   Copyright (C) 2011-2016  Brigitte Bigi
#
#                   This banner notice must not be removed
# ---------------------------------------------------------------------------
# Use of this software is governed by the GNU Public License, version 3.
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
# File: basicalign.py
# ----------------------------------------------------------------------------

from annotations.Align.aligners.basealigner import BaseAligner
from annotations.Align.aligners.alignerio   import AlignerIO

import audiodata.aio

# ----------------------------------------------------------------------------
BASIC_EXT_OUT = ["palign"]
DEFAULT_EXT_OUT = BASIC_EXT_OUT[0]
# ----------------------------------------------------------------------------

class BasicAligner( BaseAligner ):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      brigitte.bigi@gmail.com
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    @summary:      Basic automatic alignment system.

    This segmentation assign the same duration to each phoneme.
    In case of phonetic variants, the first shortest phonetization is selected.

    """
    def __init__(self, modeldir):
        """
        Constructor.

        BasicAlign aligns one inter-pausal unit with the same duration
        for each phoneme. It selects the shortest in case of variants.

        @param modeldir (str) the acoustic model file name

        """
        BaseAligner.__init__(self, modeldir)
        self._outext = DEFAULT_EXT_OUT

    # -----------------------------------------------------------------------

    def set_outext(self, ext):
        """
        Set the extension for output files.

        @param str

        """
        ext = ext.lower()
        if not ext in BasicAligner.BASIC_EXT_OUT:
            raise ValueError("%s is not a valid file extension for BasicAligner"%ext)

        self._outext = ext

    # -----------------------------------------------------------------------

    def run_alignment(self, inputwav, outputalign):
        """
        Perform the speech segmentation.
        Assign the same duration to each phoneme.

        @param inputwav (str or float) the audio input file name, of type PCM-WAV 16000 Hz, 16 bits; or its duration
        @param outputalign (str) the output file name

        @return Empty string.

        """
        if isinstance(inputwav, float) is True:
            duration = inputwav
        else:
            try:
                wavspeech = audiodata.aio.open( inputwav )
                duration  = wavspeech.get_duration()
            except Exception:
                duration = 0.

        self.run_basic(duration, outputalign)

        return ""

    # ------------------------------------------------------------------------

    def run_basic(self, duration, outputalign=None):
        """
        Perform the speech segmentation.

        Assign the same duration to each phoneme.

        @param duration (float) the duration of the audio input
        @param outputalign (str) the output file name

        @return the List of tuples (begin, end, phone)

        """
        # Remove variants: Select the first-shorter pronunciation of each token
        phoneslist = []
        phonetization = self._phones.strip().split()
        tokenization  = self._tokens.strip().split()
        selectphonetization = []
        delta = 0.
        for pron in phonetization:
            token = self.__select(pron)
            phoneslist.extend( token.split("-") )
            selectphonetization.append( token.replace("-"," ") )

        # Estimate the duration of a phone (in centi-seconds)
        if len(phoneslist) > 0:
            delta = ( duration / float(len(phoneslist)) ) * 100.

        # Generate the result
        if delta < 1. or len(selectphonetization) == 0:
            return self.gen_alignment([], [], [], int(duration*100.), outputalign)

        return self.gen_alignment(selectphonetization, tokenization, phoneslist, int(delta), outputalign)

    # ------------------------------------------------------------------------

    def gen_alignment(self, phonetization, tokenization, phoneslist, phonesdur, outputalign=None):
        """
        Write an alignment in an output file.

        @param phonetization (list) phonetization of each token
        @param tokenization (list) each token

        @param phoneslist (list) each phone
        @param phonesdur (int) the duration of each phone in centi-seconds
        @param outputalign (str) the output file name

        """
        timeval = 0
        alignments = []
        for phon in phoneslist:
            tv1 = timeval
            tv2 = timeval + phonesdur - 1
            alignments.append( (tv1, tv2, phon) )
            timeval = tv2 + 1

        if len(alignments) == 0:
            alignments = [(0, int(phonesdur), "")]

        if outputalign is not None:
            outputalign = outputalign + "." + self._outext
            alignio = AlignerIO()
            alignio.write_palign(phonetization, tokenization, alignments, outputalign)

        return alignments

    # ------------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------------

    def __select(self, pron):
        """
        Return the first of the shortest pronunciations of an entry.

        """
        tab = pron.split("|")
        i = 0
        m = len(tab[0])

        for n,p in enumerate(tab):
            if len(p) < m:
                i = n
                m = len(p)

        return tab[i].strip()

    # ------------------------------------------------------------------------
