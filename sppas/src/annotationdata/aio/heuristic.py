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


from text import RawText, CSV
from praat import TextGrid, PitchTier, IntensityTier
from signaix import HzPitch
from transcriber import Transcriber
from xra import XRA
from phonedit import Phonedit
from htk import Label, MasterLabel
from subtitle import SubRip, SubViewer
from sclite import TimeMarkedConversation, SegmentTimeMark
from elan import Elan
from xtrans import Xtrans
from annotationpro import Antx

class HeuristicFactory(object):
    __OPTS = [
        TextGrid,
        IntensityTier,
        PitchTier,
        Transcriber,
        XRA,
        # Phonedit,
        # Label,
        # MasterLabel,
        # SubRip,
        # SubViewer,
        # TimeMarkedConversation,
        # SegmentTimeMark,
        # Elan,
        Xtrans,
        Antx,
        CSV,
        HzPitch,
        RawText  # must be last
    ]

    @staticmethod
    def NewTrs(filename):
        """
        Return a new Transcription.

        @param trs_type:

        @return Transcription

        """
        for type in HeuristicFactory.__OPTS:
            try:
                if type.detect(filename):
                    return type()
            except Exception:
                continue

    # End NewTrs
    # -----------------------------------------------------------------
