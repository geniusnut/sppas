#!/usr/bin/env python2
# -*- coding: utf8 -*-

import unittest
import os.path
import shutil

from resources.vocab import Vocabulary
from sp_glob import RESOURCES_PATH
import utils.fileutils

# ---------------------------------------------------------------------------

VOCAB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "vocab.txt")
ITA = os.path.join(RESOURCES_PATH, "vocab", "ita.vocab")

TEMP = utils.fileutils.gen_name()
VOCAB_TEST = os.path.join(TEMP, "vocab.txt")

# ---------------------------------------------------------------------------


class TestVocabulary(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEMP) is False:
            os.mkdir(TEMP)

    def tearDown(self):
        shutil.rmtree(TEMP)

    def test_all(self):
        l = Vocabulary(VOCAB, nodump=True)
        self.assertEqual(l.get_size(), 20)
        self.assertTrue(l.is_unk('toto'))
        self.assertFalse(l.is_unk('normale'))
        self.assertFalse(l.is_unk("isn't"))
        self.assertFalse(l.is_unk(u"đ"))
        l.add(u"être")
        self.assertTrue(l.is_in(u"être"))
        self.assertTrue(l.is_unk("être"))

    def test_save(self):
        l = Vocabulary(VOCAB, nodump=True)
        l.save(VOCAB_TEST)
        l2 = Vocabulary(VOCAB_TEST, nodump=True)
        self.assertEqual(l.get_size(), l2.get_size())
        for w in l.get_list():
            self.assertTrue(l2.is_in(w))

    def test_ita(self):
        l = Vocabulary(ITA, nodump=True)
        self.assertTrue(l.is_unk('toto'))
        self.assertFalse(l.is_unk(u'perché'))
