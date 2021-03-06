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
# File: frameinterval.py
# ----------------------------------------------------------------------------

import baseplacement
import duration
from framepoint import FramePoint

# ----------------------------------------------------------------------------

__docformat__ = """epytext"""
__authors__ = """Brigitte Bigi (brigitte.bigi@gmail.com)"""
__copyright__ = """Copyright (C) 2011-2015  Brigitte Bigi"""

# ----------------------------------------------------------------------------

class FrameInterval(baseplacement.BasePlacement):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL, version 3
    @summary: This class is the FrameInterval representation.

    A frame interval is identified by two FramePoint objects:
        - a begin frame;
        - an end frame.

    """

    def __init__(self, begin, end):
        """
        Create a new FrameInterval instance.

        @param begin (FramePoint) start frame in seconds
        @param end (FramePoint) end frame in seconds
        @raise TypeError:
        @raise ValueError

        """

        if isinstance(begin, FramePoint) is False:
            raise TypeError(
                "FramePoint argument required for begin, not %r" % begin)

        if isinstance(end, FramePoint) is False:
            raise TypeError(
                "FramePoint argument required for end, not %r" % end)

        if(
            begin.GetMidpoint() >= end.GetMidpoint() or (
                begin.GetMidpoint()-begin.GetRadius() >
                end.GetMidpoint()-end.GetRadius())
        ):
            raise ValueError("End FramePoint must be strictly greater than "
                             "Begin FramePoint (see FramePoint definition). "
                             "(%s, %s)" % (begin, end))

        self.__begin = begin
        self.__end = end

    # -----------------------------------------------------------------------

    def Set(self, other):
        """
        Set the FrameInterval instance to new FrameInterval.

        @param other (FrameInterval)

        """
        if isinstance(other, FrameInterval) is False:
            raise TypeError("FrameInterval argument required, not %r" % other)

        other = other.Copy()
        self.__begin = other.__begin
        self.__end = other.__end

    # -----------------------------------------------------------------------

    def GetBegin(self):
        """
        Return the begin FramePoint instance.

        """
        return self.__begin

    # -----------------------------------------------------------------------

    def SetBegin(self, fp):
        """
        Set the begin FramePoint instance to a new FramePoint.

        Attention: it is a reference assignment.
        Different usage:
            - interval.SetBegin( fp )
            - interval.SetBegin( fp.Copy() )

        @param fp (FramePoint)

        """
        if isinstance(fp, FramePoint) is False:
            raise TypeError("FramePoint argument required, not %r" % fp)

        if(
            fp.GetMidpoint() >= self.__end.GetMidpoint() or (
                fp.GetMidpoint()-fp.GetRadius() >
                self.__end.GetMidpoint()-self.__end.GetRadius())
           ):
            raise ValueError("End FramePoint must be strictly greater than "
                             "Begin FramePoint (see FramePoint definition). "
                             "(%s, %s)" % (fp, self.__end))

        self.__begin = fp  # assign the reference

    # -----------------------------------------------------------------------

    def GetEnd(self):
        """
        Return the end FramePoint instance.

        """
        return self.__end

    # -----------------------------------------------------------------------

    def SetEnd(self, fp):
        """
        Set the end FramePoint instance to a new FramePoint.

        @param fp (FramePoint)

        """
        if isinstance(fp, FramePoint) is False:
            raise TypeError("FramePoint argument required, not %r" % fp)

        if(
            self.__begin.GetMidpoint() >= fp.GetMidpoint() or (
                self.__begin.GetMidpoint()-self.__begin.GetRadius() >
                fp.GetMidpoint()-fp.GetRadius())
        ):
            raise ValueError("End FramePoint must be strictly greater than"
                             " Begin FramePoint (see FramePoint definition)."
                             " (%s, %s)" % (self.__begin, fp))

        self.__end = fp  # assign the reference

    # -----------------------------------------------------------------------

    def IsInterval(self):
        """
        Return True, because self is representing an interval.

        """
        return True

    # -----------------------------------------------------------------------

    def IsFrameInterval(self):
        """
        Return True, because self is an instance of FrameInterval.

        """
        return True

    # -----------------------------------------------------------------------

    def Copy(self):
        """
        Return a deep copy of self.

        """
        b = self.__begin.Copy()
        e = self.__end.Copy()
        return FrameInterval(b, e)

    # -----------------------------------------------------------------------

    def Duration(self):
        """
        Return the duration of the interval, in number of frames,
        without taking into account the radius.

        """
        # duration is the difference between the midpoints
        value = self.__end.GetMidpoint() - self.__begin.GetMidpoint()
        # vagueness of the duration is based on begin/end radius values
        vagueness = self.__begin.GetRadius() + self.__end.GetRadius()

        return duration.Duration(value,vagueness)

    # ------------------------------------------------------------------------------------

    def Combine(self, other):
        """
        Return a FrameInterval, the combination of two intervals.

        @param other (FrameInterval)
        is the other frame interval to be combined with.

        """
        if isinstance(other, FrameInterval) is False:
            raise TypeError("FrameInterval argument required, not %r" % other)

        if self > other:
            other, self = self, other

        if self.__end <= other.GetBegin():
            return FrameInterval(self.__begin, other.GetEnd())

        return FrameInterval(other.GetBegin(), self.__end)

    # -----------------------------------------------------------------------

    def Union(self, other):
        """
        Return a FrameInterval representing the union of two intervals.

        @param other (FrameInterval) is the interval to merge with.

        """
        if isinstance(other, FrameInterval) is False:
            raise TypeError("FrameInterval argument required, not %r" % other)

        if self > other:
            other, self = self, other

        return FrameInterval(self.__begin, other.GetEnd())

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __repr__(self):
        return "FrameInterval: [%s,%s]" % (self.__begin, self.__end)

    # -----------------------------------------------------------------------

    def __str__(self):
        return "[%s,%s]" % (self.__begin, self.__end)

    # -----------------------------------------------------------------------

    def __contains__(self, other):
        """
        Return True if the given frame point is contained in the interval.

        @param other is the other frame point to compare with.

        """
        if isinstance(other, (FrameInterval, FramePoint, int,)) is False:
            raise TypeError(
                "%r cannot be compared with FrameInterval." % other)

        if isinstance(other, FrameInterval) is True:
            return (self.__begin <= other.GetBegin() and
                    other.GetEnd() <= self.__end)

        return self.__begin <= other <= self.__end

    # -----------------------------------------------------------------------

    def __eq__(self, other):
        """
        Equal.

        @param other (FrameInterval) is the other frame point to compare with.

        """
        if isinstance(other, FrameInterval) is False:
            return False

        return (self.__begin == other.GetBegin() and
                self.__end == other.GetEnd())

    # -----------------------------------------------------------------------

    def __lt__(self, other):
        """
        LowerThan.

        @param other (FrameInterval, FramePoint, int)
        is the other frame point to compare with.

        """
        if isinstance(other, (FramePoint, int)):
            return self.__end < other

        if isinstance(other, FrameInterval) is False:
            return False

        return self.__begin < other.GetBegin()

    # -----------------------------------------------------------------------

    def __gt__(self, other):
        """
        GreaterThan.

        @param other (FrameInterval, FramePoint, int)
        is the other frame point to compare with.

        """
        if isinstance(other, (int, FramePoint)):
            return self.__begin > other

        if isinstance(other, FrameInterval) is False:
            return False

        return self.__begin > other.GetBegin()

    # -----------------------------------------------------------------------
