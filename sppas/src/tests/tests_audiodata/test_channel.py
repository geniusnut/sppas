#!/usr/bin/env python2
# -*- coding: utf8 -*-

import sys
from os.path import abspath, dirname
SPPAS = dirname(dirname(dirname(abspath(__file__))))
sys.path.append( SPPAS )

import unittest
import os

import audiodata.io
from audiodata.channel import Channel
from audiodata.audio import AudioPCM
from tests.paths import SPPASSAMPLES, TEMP

sample_1 = os.path.join(SPPASSAMPLES, "samples-eng", "oriana1.wav")  # mono
sample_2 = os.path.join(SPPASSAMPLES, "samples-eng", "oriana3.wave") # stereo
sample_3 = os.path.join(SPPASSAMPLES, "samples-fra", "F_F_B003-P9.wav")
sample_new = os.path.join(TEMP, "converted.wav")

class TestChannel(unittest.TestCase):

    def setUp(self):
        self._sample_1 = audiodata.io.open(sample_1)
        self._sample_2 = audiodata.io.open(sample_2)
        self._sample_3 = audiodata.io.open(sample_3)

    def tearDown(self):
        self._sample_1.close()

    def test_Extract(self):
        frames = self._sample_1.read_frames( self._sample_1.get_nframes() )
        self._sample_1.rewind()
        cidx = self._sample_1.extract_channel(0)
        channel = self._sample_1.get_channel(cidx)
        self.assertEqual(len(frames)/self._sample_1.get_sampwidth(), channel.get_nframes())
        self.assertEqual(frames, channel.frames)
        self.assertEqual(frames, channel.get_frames(channel.get_nframes()))

        frames = self._sample_2.read_frames( self._sample_2.get_nframes() )
        frameschannel = ""
        #we are going to extract the channel number 2, so we have to skip all frames which belong to the channel number 1
        for i in xrange(self._sample_2.get_sampwidth(), len(frames), self._sample_2.get_sampwidth()*self._sample_2.get_nchannels()):
            for j in xrange(self._sample_2.get_sampwidth()):
                frameschannel += frames[i+j]
        self._sample_2.rewind()
        #Channel number 2 have index 1
        cidx = self._sample_2.extract_channel(1)
        channel = self._sample_2.get_channel(cidx)
        self.assertEqual(len(frameschannel)/self._sample_2.get_sampwidth(), channel.get_nframes())
        self.assertEqual(frameschannel, channel.frames)
        self.assertEqual(frameschannel, channel.get_frames(channel.get_nframes()))

    def test_GetFrames(self):
        self._sample_1.set_pos(1000)
        frames = self._sample_1.read_frames( 500 )
        self._sample_1.rewind()
        cidx = self._sample_1.extract_channel(0)
        channel = self._sample_1.get_channel(cidx)
        self.assertEqual(len(frames)/self._sample_1.get_sampwidth(), 500)
        channel.seek(1000)
        self.assertEqual(channel.tell(), 1000)
        self.assertEqual(frames, channel.get_frames(500))

    def test_Save(self):
        cidx = self._sample_1.extract_channel(0)
        channel = self._sample_1.get_channel(cidx)
        audio = AudioPCM()
        audio.append_channel( channel )
        audiodata.io.save( sample_new, audio )
        savedaudio = audiodata.io.open( sample_new )

        self._sample_1.rewind()
        frames = self._sample_1.read_frames( self._sample_1.get_nframes() )
        savedframes = savedaudio.read_frames( self._sample_1.get_nframes() )
        self.assertEqual(len(frames), len(savedframes))
        self.assertEqual(frames, savedframes)

        savedaudio.close()
        os.remove( sample_new )

    def test_ExtractFragment(self):
        self._sample_1.extract_channel(0)
        self._sample_3.extract_channel(0)

        channel = self._sample_1.get_channel(0)
        newchannel = channel.extract_fragment(1*channel.get_framerate(),2*channel.get_framerate())
        self.assertEqual(newchannel.get_nframes()/newchannel.get_framerate(), 1)