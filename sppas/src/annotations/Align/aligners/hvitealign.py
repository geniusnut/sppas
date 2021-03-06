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
# File: hvitealign.py
# ---------------------------------------------------------------------------

import os
import codecs
from subprocess import Popen, PIPE, STDOUT

from annotations.Align.aligners.basealigner import BaseAligner

from sp_glob import encoding
from resources.dictpron import DictPron

# ----------------------------------------------------------------------------
HVITE_EXT_OUT = ["mlf"]
DEFAULT_EXT_OUT = HVITE_EXT_OUT[0]
# ----------------------------------------------------------------------------

class HviteAligner( BaseAligner ):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      brigitte.bigi@gmail.com
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    @summary:      HVite automatic alignment system.

    http://htk.eng.cam.ac.uk/links/asr_tool.shtml

    """
    def __init__(self, modeldir):
        """
        Constructor.

        HviteAligner aligns one inter-pausal unit.

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
        if not ext in HVITE_EXT_OUT:
            raise ValueError("%s is not a valid file extension for HVitesAligner"%ext)

        self._outext = ext

    # -----------------------------------------------------------------------

    def gen_dependencies(self, grammarname, dictname):
        """
        Generate the dependencies (grammar, dictionary) for HVite.

        @param grammarname is the file name of the tokens
        @param dictname is the dictionary file name

        """
        dictpron = DictPron()

        with codecs.open(grammarname, 'w', encoding) as flab:

            for token,pron in zip(self._tokens.split(),self._phones.split()):

                # dictionary:
                for variant in pron.split("|"):
                    dictpron.add_pron( token, variant.replace("-"," ") )
                    if self._infersp is True:
                        variant = variant + '-sil'
                        dictpron.add_pron( token, variant.replace("-"," ") )

                # lab file (one token per line)
                flab.write( token+"\n")

        dictpron.save_as_ascii( dictname )

    # -----------------------------------------------------------------------

    def run_hvite(self, inputwav, outputalign):
        """
        Perform the speech segmentation.
        Call the system command `HVite`.

        @param inputwav (str - IN) the audio input file name, of type PCM-WAV 16000 Hz, 16 bits
        @param outputalign (str - OUT) the output file name

        """
        basename = os.path.splitext(inputwav)[0]
        dictname = basename + ".dict"
        grammarname = basename + ".lab"
        self.gen_dependencies(grammarname, dictname)

        # Example of use with triphones:
        #
        # HVite
        #   -A                             # print command line arguments
        #   -D                             # display configuration variables
        #   -T 1                           # set trace flags to N
        #   -l '*'                         # dir to store label/lattice files
        #   -a                             # align from label file
        #   -b SENT-END                    # *** TO NOT USE for forced-alignment ***
        #   -m                             # output model alignment
        #   -C models-EN/config            # model config !IMPORTANT!
        #   -H models-EN/macros
        #   -H models-EN/hmmdefs
        #   -t 250.0 150.0 1000.0
        #   -i aligned.out
        #   -y lab
        #   dict/EN.dict
        #   models-EN/tiedlist
        #   file.wav
        #
        # Replace the tiedlist by the list of phonemes for a monophone model

        hmmdefs  = os.path.join(self._model, "hmmdefs")
        macros   = os.path.join(self._model, "macros")
        config   = os.path.join(self._model, "config")
        graph    = os.path.join(self._model, "tiedlist")
        if os.path.isfile(graph) is False:
            graph = os.path.join(self._model, "monophones")

        # Program name
        command = "HVite "
        command += " -T 1 "
        command += " -l '*' "
        command += " -a "
        command += " -m "
        command += ' -C "' + config.replace('"', '\\"') + '" '
        command += ' -H "' + hmmdefs.replace('"', '\\"') + '" '
        if os.path.isfile(macros):
            command += ' -H "' + macros.replace('"', '\\"') + '" '
        command += " -t 250.0 150.0 1000.0 "
        command += ' -i "' + outputalign.replace('"', '\\"') + '" '
        command += ' -y lab'
        command += ' "' + dictname.replace('"', '\\"') + '" '
        command += ' "' + graph.replace('"', '\\"') + '" '
        command += inputwav

        # Execute command
        p = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        p.wait()
        line = p.communicate()

        if len(line[0]) > 0 and line[0].find("not found") > -1:
            raise OSError( "HVite is not properly installed. See installation instructions for details." )

        if len(line[0]) > 0 and line[0].find("ERROR [") > -1:
            raise OSError( "HVite command failed." )

        # Check output file
        if os.path.isfile( outputalign ) is False:
            raise Exception('HVite did not created an alignment file.')

    # -----------------------------------------------------------------------

    def run_alignment(self, inputwav, outputalign):
        """
        Execute the external program `HVite` to align.

        @param inputwav (str - IN) the audio input file name, of type PCM-WAV 16000 Hz, 16 bits
        @param outputalign (str - OUT) the output file name

        @return (str) An empty string.

        """
        outputalign = outputalign + "."  + self._outext

        self.run_hvite(inputwav, outputalign)

        if os.path.isfile(outputalign):
            with codecs.open(outputalign, 'r', encoding) as f:
                lines = f.readlines()
                if len(lines) == 1:
                    raise Exception(lines)

        return ""

    # -----------------------------------------------------------------------
