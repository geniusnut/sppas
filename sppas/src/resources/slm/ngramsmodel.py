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
# File: ngramsmodel.py
# ---------------------------------------------------------------------------

import collections
import math

import annotationdata
from resources.vocab import Vocabulary
from sp_glob import UNKSTAMP

# ---------------------------------------------------------------------------

MAX_ORDER = 20
START_SENT_SYMBOL = "<s>"
END_SENT_SYMBOL   = "</s>"

# ---------------------------------------------------------------------------


class NgramsModel(object):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      brigitte.bigi@gmail.com
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    @summary:      Statistical language model trainer.

    A model is made of:
       - n-gram counts: a list of NgramCounter instances.
       - n-gram probabilities.

    How to estimate n-gram probabilities?

    A slight bit of theory...
    The following is copied (cribbed!) from the SRILM following web page:
    http://www.speech.sri.com/projects/srilm/manpages/ngram-discount.7.html

       a_z    An N-gram where a is the first word, z is the last word, and "_"
              represents 0 or more words in between.

       c(a_z)  The count of N-gram a_z in the training data

       p(a_z) The estimated conditional probability of the nth word z given the
              first n-1 words (a_) of an N-gram.

       a_     The n-1 word prefix of the N-gram a_z.
       _z     The n-1 word suffix of the N-gram a_z.

    N-gram models try to estimate the probability of a word z in the context of
    the previous n-1 words (a_).
    One way to estimate p(a_z) is to look at the number of times word z has
    followed the previous n-1 words (a_):
        (1) p(a_z) = c(a_z)/c(a_)
    This is known as the maximum likelihood (ML) estimate. Notice that it
    assigns zero probability to N-grams that have not been observed in the
    training data.

    To avoid the zero probabilities, we take some probability mass from the
    observed N-grams and distribute it to unobserved N-grams. Such
    redistribution is known as smoothing or discounting. Most existing
    smoothing algorithms can be described by the following equation:
        (2)  p(a_z) = (c(a_z) > 0) ? f(a_z) : bow(a_) p(_z)
    If the N-gram a_z has been observed in the training data, we use the
    distribution f(a_z). Typically f(a_z) is discounted to be less than the
    ML estimate so we have some leftover probability for the z words unseen
    in the context (a_). Different algorithms mainly differ on how they
    discount the ML estimate to get f(a_z).

    How to use this class?

    >>> model = NgramsModel(3)                         # create a 3-gram model
    >>> model.count( *corpusfiles )                    # count n-grams from data
    >>> probas = model.probabilities(method="logml")   # estimates probas

    """
    def __init__(self, norder=1):
        """
        Constructor.

        @param norder (int) n-gram order, between 1 and MAX_ORDER.

        """
        n = int(norder)
        if n < 1:
            raise ValueError('Expected order between 1 and %d. Get: %d.'%(MAX_ORDER,n))
        self.order = n
        self._ngramcounts = []

        self._ss = START_SENT_SYMBOL
        self._es = END_SENT_SYMBOL

        # Options
        self.vocab    = None    # list of tokens of the unigram model
        self.mincount = 1       # minimum number of occurrences
        self.wrdlist  = None    # vocabulary

    # -----------------------------------------------------------------------

    def get_order(self):
        """
        Return the n-gram order value.

        @return N-gram order integer value to assign.

        """
        return self.order

    # -----------------------------------------------------------------------

    def set_start_symbol(self, symbol):
        """
        Set the start sentence symbol.

        @param symbol (str - IN)

        """
        s = str(symbol).strip()
        if len(s) > 0:
            self._ss = s

    # -----------------------------------------------------------------------

    def set_end_symbol(self, symbol):
        """
        Set the end sentence symbol.

        @param symbol (str - IN)

        """
        e = str(symbol).strip()
        if len(e) > 0:
            self._es = e

    # -----------------------------------------------------------------------

    def set_vocab(self, filename):
        """
        Fix a list of accepted tokens; others are mentioned as unknown.

        @param filename (str - IN) List of tokens.

        """
        self.wrdlist = Vocabulary(filename, nodump=True, case_sensitive=False)

    # -----------------------------------------------------------------------

    def count(self, *datafiles):
        """
        Count ngrams from data files.

        @param datafiles (*args - IN) is a set of file names, with UTF-8 encoding.
        If the file contains more than one tier, only the first one is used.

        """
        self._create_counters()

        for ngramcounter in self._ngramcounts:
            ngramcounter.count( *datafiles )

        # We already fixed a count threshold
        if self.mincount > 1:
            self._ngramcounts[-1].shave(self.mincount)

    # -----------------------------------------------------------------------

    def append_sentences(self, sentences):
        """
        Append a list of sentences in data counts.

        @param sentence (list - IN) sentences with tokens separated by whitespace.

        """
        self._create_counters()

        for ngramcounter in self._ngramcounts:
            for sentence in sentences:
                ngramcounter.append_sentence( sentence )

    # -----------------------------------------------------------------------

    def set_min_count(self, value):
        """
        Fix a minimum count values, applied only to the max order.
        Any observed n-gram with a count under the value is removed.

        @param value (int - IN) Threshold for minimum count

        """
        value = int(value)
        if value < 1:
            raise Exception('Expected a count value > 1. Got %d'%value)

        # We already have counts
        if len(self._ngramcounts) > 0:
            self._ngramcounts[-1].shave(value)

        self.mincount = value

    # -----------------------------------------------------------------------

    def probabilities(self, method="lograw"):
        """
        Return a list of probabilities.

        @param method (str) method to estimate probabilities, i.e. one of:

            - raw:    return counts instead of probabilities
            - lograw: idem with log values

            - ml:     return maximum likelihood (un-smoothed probabilities)
            - logml:  idem with log values

        @return list of n-gram probabilities.
        Example:
            >>> probas = probabilities("logml")
            >>> for t in probas[0]:
            >>>      print t
            ('</s>', -1.066946789630613, None)
            ('<s>', -99.0, None)
            (u'a', -0.3679767852945944, None)
            (u'b', -0.5440680443502756, None)
            (u'c', -0.9420080530223132, None)
            (u'd', -1.066946789630613, None)

        """
        method = str(method).strip().lower()

        if method == "raw":
            return self._probas_as_raw( tolog=False )

        if method == "lograw":
            return self._probas_as_raw( tolog=True )

        if method == "ml":
            return self._probas_as_ml( tolog=False )

        if method == "logml":
            return self._probas_as_ml( tolog=True )

        raise ValueError('Expected a method name. Got: %s'%(method))

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def _create_counters(self):
        """
        Create empty counters.
        Erase existing ones if any (except if order didn't changed)!

        """
        if len(self._ngramcounts) != self.order:
            for n in range(self.order):
                ngramcounter = NgramCounter(n+1, self.wrdlist)
                self._ngramcounts.append( ngramcounter )

    # -----------------------------------------------------------------------

    def _probas_as_raw(self, tolog=True):
        """
        Do not estimate probas... just return raw counts.

        """
        models = []

        for n in range(len(self._ngramcounts)):

            ngram = []
            for entry in self._ngramcounts[n].get_ngrams():
                token = " ".join(entry)
                c = self._ngramcounts[n].get_count(token)
                if token == self._ss and tolog is True:
                    ngram.append((self._ss,-99,None))
                else:
                    if tolog is False:
                        ngram.append((token,c,None))
                    else:
                        ngram.append((token,math.log(c,10.),None))
            models.append(ngram)

        return models

    def _probas_as_ml(self, tolog=True):
        """
        Estimates probas with maximum likekihood method.

        (1) p(a_z) = c(a_z)/c(a_)

        """
        models = []

        for n in range(len(self._ngramcounts)):
        # n is the index in ngramcounts, i.e. the expected order-1.

            ngram = []
            oldhist = ""
            for entry in self._ngramcounts[n].get_ngrams():

                # Estimates c(a_)
                if n == 0:
                    # unigrams
                    total = float(self._ngramcounts[n].get_ncount())
                else:
                    hist = " ".join(entry[:-1])
                    hist = hist.strip()
                    if hist != oldhist:
                        if hist == self._ss:
                            total = float(self._ngramcounts[n-1].get_count(self._es))
                        else:
                            total = float(self._ngramcounts[n-1].get_count(hist))

                # Estimates c(a_z)
                token = " ".join(entry)
                c = self._ngramcounts[n].get_count(token)

                # Estimates p(a_z)
                f = float(c) / total

                # bow
                bow = None
                if n < (len(self._ngramcounts)-1):
                    bow = 0
                    if token == self._es:
                        bow = -99

                # Adjust f if unigram(start-sent), then append
                if token == self._ss:
                    if tolog is True:
                        ngram.append((self._ss,-99.,bow))
                    else:
                        ngram.append((self._ss,0.,bow))
                else:
                    if tolog is False:
                        ngram.append((token,f,bow))
                    else:
                        ngram.append((token,math.log(f,10.),bow))

            models.append(ngram)

        return models

# ---------------------------------------------------------------------------


class NgramCounter(object):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      brigitte.bigi@gmail.com
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    @summary:      N-gram representation.

    """
    def __init__(self, n=1, wordslist=None):
        """
        Constructor.

        @param n (int) n-gram order, between 1 and MAX_ORDER.
        @param wordslist (Vocabulary) a list of accepted tokens.

        """
        n = int(n)
        if n < 1:
            raise ValueError('Expected order between 1 and %d. Got: %d.'%(MAX_ORDER,n))
        self._n      = n   # n-gram order to count
        self._ss     = START_SENT_SYMBOL
        self._es     = END_SENT_SYMBOL
        self._datacounts = collections.defaultdict(lambda: None)
        self._wordslist = wordslist
        self._nsent  = 0   # number of sentences (estimated)
        self._ncount = 0   # number of observed n-grams (estimated)

    # -----------------------------------------------------------------------

    def get_ngrams(self):
        """
        Get the list of alphabetically-ordered n-grams.

        @return list of tuples

        """
        return sorted( self._datacounts.keys() )

    # -----------------------------------------------------------------------

    def get_ngram_count(self, ngram):
        """
        Get the count of a specific ngram.

        @param ngram (tuple of str - IN) Tuple of tokens.

        """
        return self._datacounts.get( ngram,0 )

    # -----------------------------------------------------------------------

    def get_count(self, sequence):
        """
        Get the count of a specific sequence.

        @param sequence (str - IN) tokens separated by whitespace.

        """
        tt = tuple(sequence.split())
        return self._datacounts.get( tt,0 )

    # -----------------------------------------------------------------------

    def get_ncount(self):
        """
        Get the number of observed n-grams, excluding start symbols if unigrams.

        @return int

        """
        return self._ncount

    # -----------------------------------------------------------------------

    def count(self, *datafiles):
        """
        Count ngrams of order n from data files.

        @param datafiles (*args - IN) is a set of file names, with UTF-8 encoding.
        If the file contains more than one tier, only the first one is used.

        """
        for filename in datafiles:
            trs = annotationdata.aio.read( filename )
            if trs.GetSize() == 0:
                continue
            tier = trs[0]
            for ann in tier:
                label = ann.GetLabel()
                if label.IsEmpty() is False and label.IsSilence() is False:
                    self.append_sentence(label.GetValue())

        if self._n == 1:
            self._datacounts[((self._ss),)] = 0

    # -----------------------------------------------------------------------

    def append_sentence(self, sentence):
        """
        Append a sentence in a dictionary of data counts.

        @param sentence (str - IN) with tokens separated by whitespace.

        """
        # get the list of observed tokens
        symbols = self._sentence_to_tokens(sentence)

        # get a list of ngrams from a list of tokens.
        ngrams = zip(*[symbols[i:] for i in range(self._n)])

        # append the list of ngrams into a dictionary of such items.
        for each in ngrams:

            v = 1 + self._datacounts.get(each,0)
            self._datacounts[each] = v

        if self._n == 1:
            self._datacounts[((self._ss),)] = 0

        self._nsent = self._nsent + 1
        self._ncount = self._ncount + len(ngrams) - 1
        # notice that we don't add count of sent-start,
        # but we add it for sent-end

    # -----------------------------------------------------------------------

    def shave(self, value):
        """
        Remove data if count is lower than the given value.

        """
        # we can't delete an item while iterating the dict.
        # so... 2 steps: we store keys to delete, then we pop them!
        topop = []
        for k,c in self._datacounts.iteritems():
            if k[0] == self._ss or k[0] == self._es:
                continue
            if c < value:
                topop.append(k)
        for k in topop:
            self._datacounts.pop(k)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def _sentence_to_tokens(self, sentence):
        """
        Return the (ordered) list of tokens of the given sentence.

        @param sentence (str - IN)
        @return list of str

        """
        # We are not using a  vocabulary
        if self._wordslist is None:
            tokens = sentence.split()
        else:
            tokens = []
            # We need to check if each token is in the vocabulary
            for token in sentence.split():
                if self._wordslist.is_in(token):
                    tokens.append(token)
                else:
                    tokens.append(UNKSTAMP)

        if tokens[0] != self._ss:
            tokens.insert( 0,self._ss )
        if tokens[-1] != self._es:
            tokens.append( self._es )
        return tokens

    # -----------------------------------------------------------------------
