# -*- coding: UTF-8 -*-
"""
    ..
        ---------------------------------------------------------------------
         ___   __    __    __    ___
        /     |  \  |  \  |  \  /              the automatic
        \__   |__/  |__/  |___| \__             annotation and
           \  |     |     |   |    \             analysis
        ___/  |     |     |   | ___/              of speech

        http://www.sppas.org/

        Use of this software is governed by the GNU Public License, version 3.

        SPPAS is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        SPPAS is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with SPPAS. If not, see <http://www.gnu.org/licenses/>.

        This banner notice must not be removed.

        ---------------------------------------------------------------------

    src.calculus.descriptivestats.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import stats.central
import stats.variability
import stats.moment

# ----------------------------------------------------------------------------


class DescriptiveStatistics(object):
    """
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    :author:       Brigitte Bigi
    :contact:      brigitte.bigi@gmail.com
    :summary:      Descriptive statistics estimator class.

    This class estimates descriptive statistics on a set of data values,
    stored in a dictionary:
    
        - the key is the name of the data set;
        - the value is the list of data values for this data set.

    >>> d = {'apples':[1, 2, 3, 4], 'peers':[2, 3, 3, 5]}
    >>> s = DescriptiveStatistics(d)
    >>> total = s.total()
    >>> print total
    >>> (('peers', 13.0), ('apples', 10.0))

    """
    def __init__(self, dict_items):
        """ Descriptive statistics.

        :param dict_items: a dict of tuples (key, [values])

        """
        self.items = dict_items

    # -----------------------------------------------------------------------

    def len(self):
        """ Estimates the number of occurrences of data values.

        :returns: (dict) a dictionary of tuples (key, len)

        """
        return dict((key, len(values)) for key,values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def total(self):
        """ Estimates the sum of data values.

        :returns: (dict) a dictionary of tuples (key, total) of float values

        """
        return dict((key, stats.central.fsum(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def min(self):
        """ Estimates the minimum of data values.

        :returns: (dict) a dictionary of (key, min) of float values

        """
        return dict((key, stats.central.fmin(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def max(self):
        """ Estimates the maximum of data values.

        :returns: (dict) a dictionary of (key, max) of float values

        """
        return dict((key, stats.central.fmax(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def mean(self):
        """ Estimates the arithmetic mean of data values.

        :returns: (dict) a dictionary of (key, mean) of float values

        """
        return dict((key, stats.central.fmean(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def median(self):
        """ Estimates the 'middle' score of the data values.

        :returns: (dict) a dictionary of (key, mean) of float values

        """
        return dict((key, stats.central.fmedian(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def variance(self):
        """
        Estimates the unbiased sample variance of data values.

        :returns: (dict) a dictionary of (key, variance) of float values

        """
        return dict((key, stats.variability.lvariance(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def stdev(self):
        """
        Estimates the standard deviation of data values.

        :returns: (dict) a dictionary of (key, stddev) of float values

        """
        return dict((key, stats.variability.lstdev(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def coefvariation(self):
        """
        Estimates the coefficient of variation of data values (given as a percentage).

        :returns: (dict) a dictionary of (key, coefvariation) of float values

        """
        return dict((key, stats.moment.lvariation(values)) for key, values in self.items.iteritems())

    # -----------------------------------------------------------------------

    def zscore(self):
        """ Estimates the z-scores of data values.
        The z-score determines the relative location of a data value.

        :returns: (dict) a dictionary of (key, [z-scores]) of float values

        """
        return dict((key, stats.variability.lzs(values)) for key, values in self.items.iteritems())
