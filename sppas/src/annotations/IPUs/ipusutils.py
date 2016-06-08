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
# File: ipusutils.py
# ---------------------------------------------------------------------------


def frames2times(listframes, framerate):
    """
    Convert a list of frame' into a list of time' values.

    @param listframes (list) tuples (from_pos,to_pos)
    @return a list of tuples (from_time,to_time)

    """
    listtimes = []
    fm = float(framerate)

    for (s,e) in listframes:
        fs = float(s) / fm
        fe = float(e) / fm
        listtimes.append( (fs, fe) )

    return listtimes

# ------------------------------------------------------------------

def times2frames(listtimes, framerate):
    """
    Convert a list of time' into a list of frame' values.

    @param listframes (list) tuples (from_time,to_time)
    @return a list of tuples (from_pos,to_pos)

    """
    listframes = []
    fm = float(framerate)
    for (s,e) in listtimes:
        fs = int(s*fm)
        fe = int(e*fm)
        listframes.append( (fs, fe) )

    return listframes

# ------------------------------------------------------------------