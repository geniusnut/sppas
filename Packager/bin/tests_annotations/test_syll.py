#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import unittest
import os
import sys
import os.path

SPPAS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(SPPAS, 'sppas', 'src'))

from annotations.Syll.syllabification import Syllabification
from sp_glob import RESOURCES_PATH
POL_SYLL = os.path.join(RESOURCES_PATH, "syll", "syllConfig-pol.txt")
FRA_SYLL = os.path.join(RESOURCES_PATH, "syll", "syllConfig-fra.txt")

from annotationdata.tier           import Tier
from annotationdata.annotation     import Annotation
from annotationdata.ptime.interval import TimeInterval
from annotationdata.ptime.point    import TimePoint
from annotationdata.label.label    import Label

# -------------------------------------------------------------------------

def labels2tier(phonemes):
    # Convert a list of strings into a tier.
    if len(phonemes)==0:
        return None
    tier = Tier('Phonemes')
    for time,p in enumerate(phonemes):
        begin = TimePoint(time)
        end   = TimePoint(time+1)
        label = Label(p)
        a = Annotation( TimeInterval(begin,end), label)
        tier.Append(a)
    return tier

# -------------------------------------------------------------------------

def get_syll(trs):
    tierS = trs.Find("Syllables")
    if tierS is None: return ""
    if tierS.GetSize()==0: return ""
    line = ""
    for s in tierS:
        text = s.GetLabel().GetValue()
        line = line+text + "|"
    return line[:-1]

# -------------------------------------------------------------------------

class TestSyll(unittest.TestCase):

    def setUp(self):
        self.syllabifierPOL = Syllabification(POL_SYLL, None)
        self.syllabifierFRA = Syllabification(FRA_SYLL, None)

    def testVV(self):
        tierP = labels2tier( ['a','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("a|a", syll)

    def testVCV(self):
        tierP = labels2tier( ['a','b','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("a|ba", syll)

    def testVCCV(self):
        # general rule
        tierP = labels2tier( ['a','n','c','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("an|ca", syll)

        # exception rule
        tierP = labels2tier( ['a','g','j','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("a|gja", syll)

        # specific (shift to left)
        tierP = labels2tier( ['a','d','g','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("a|dga", syll)

        # do not apply the previous specific rule if not VdgV
        tierP = labels2tier( ['a','x','d','g','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("ax|dga", syll)

        # specific (shift to right)
        tierP = labels2tier( ['a','z','Z','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("az|Za", syll)


    def testVCCCV(self):
        # general rule
        tierP = labels2tier( ['a','m','m','n','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("am|mna", syll)

        # exception rule
        tierP = labels2tier( ['a','dz','v','j','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("a|dzvja", syll)

        # specific (shift to left)
        tierP = labels2tier( ['a','b','z','n','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("a|bzna", syll)

        # specific (shift to right)
        tierP = labels2tier( ['a','r','w','S','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierPOL.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("arw|Sa", syll)


    def testVCCCCCV(self):
        tierP = labels2tier( ['a','p','s','k','m','w','a'] )
        self.assertIsNotNone(tierP)
        trsS = self.syllabifierFRA.syllabify( tierP )
        syll = get_syll(trsS)
        self.assertEqual("apsk|mwa", syll)


# End TestSyll
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSyll)
    unittest.TextTestRunner(verbosity=2).run(suite)
