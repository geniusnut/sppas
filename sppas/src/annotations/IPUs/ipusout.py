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
# File: ipusout.py
# ---------------------------------------------------------------------------

import codecs
import os

from sp_glob import encoding

from audiodata.autils import frames2times

import audiodata.aio
import annotationdata.aio
from audiodata.audio                import AudioPCM
from annotationdata.transcription   import Transcription
from annotationdata.media           import Media
from annotationdata.ptime.point     import TimePoint
from annotationdata.ptime.interval  import TimeInterval
from annotationdata.label.label     import Label
from annotationdata.annotation      import Annotation

# ---------------------------------------------------------------------------

class IPUsOut( object ):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      brigitte.bigi@gmail.com
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    @summary:      Writer for IPUs.

    """
    def __init__(self, tracks):
        """
        Creates a new IPUsOut instance.

        """
        super(IPUsOut, self).__init__()
        self.set_tracks(tracks)

    # ------------------------------------------------------------------
    # Manage Tracks
    # ------------------------------------------------------------------

    def check_tracks(self, tracks):
        """
        Checks if the given list of tracks is okay.
        Raise exception if error.

        """
        return [(int(s),int(e)) for (s,e) in tracks]

    # ------------------------------------------------------------------

    def set_tracks(self, tracks):
        """
        Set a new list of tracks.

        """
        if tracks is not None:
            self.tracks = self.check_tracks(tracks)
        else:
            self.tracks = []

    # ------------------------------------------------------------------
    # Convert methods
    # ------------------------------------------------------------------

    def tracks2transcription(self, ipustrs, ipusaudio, addipuidx=False):
        """
        Create a Transcription object from tracks.

        """
        if len(self.tracks) == 0:
            raise IOError('No IPUs to write.\n')

        # Extract the info we need from ipusaudio
        framerate = ipusaudio.get_channel().get_framerate()
        end_time  = ipusaudio.get_channel().get_duration()

        # Extract the info we need from ipustrs
        try:
            medialist = ipustrs.trsinput.GetMedia()
            if len(medialist) > 0:
                media = medialist[0]
            else:
                media = None
        except Exception:
            media = None
        units = ipustrs.get_units()
        if len(units) != 0:
            if len(self.tracks) != len(units):
                raise Exception('Bad number of tracks and units. Got %d tracks, and %d units.\n'%(len(self.tracks),len(units)))

        # Create the transcription and tiers
        trs = Transcription("IPU-Segmentation")
        tieripu = trs.NewTier("IPUs")
        tier    = trs.NewTier("Transcription")
        radius  = 1.0 / framerate

        # Convert the tracks: from frames to times
        trackstimes = frames2times(self.tracks, framerate)
        i = 0
        to_prec = 0.

        for (from_time,to_time) in trackstimes:

            # From the previous track to the current track: silence
            if to_prec < from_time:
                begin = to_prec
                end   = from_time
                a     = Annotation(TimeInterval(TimePoint(begin,radius), TimePoint(end,radius)), Label("#"))
                tieripu.Append(a)
                tier.Append(a.Copy())

            # New track with speech
            begin = from_time
            end   = to_time

            # ... IPU tier
            label = "ipu_%d"%(i+1)
            a  = Annotation(TimeInterval(TimePoint(begin,radius), TimePoint(end,radius)), Label(label))
            tieripu.Append(a)

            # ... Transcription tier
            if addipuidx is False:
                label = ""
            if len(units) > 0:
                label = label + " " + units[i]
            a  = Annotation(TimeInterval(TimePoint(begin,radius), TimePoint(end,radius)), Label(label))
            tier.Append(a)

            # Go to the next
            i += 1
            to_prec = to_time

        # The end is a silence?
        if to_prec < end_time:
            begin = TimePoint(to_prec,radius)
            end   = TimePoint(end_time,radius)
            if begin < end:
                a  = Annotation(TimeInterval(begin, end), Label("#"))
                tieripu.Append(a)
                tier.Append(a.Copy())

        # Link both tiers: IPU and Transcription
        try:
            trs.GetHierarchy().add_link('TimeAssociation', tieripu, tier)
        except Exception:
            pass

        # Set media
        if media is not None:
            trs.AddMedia( media )
            for tier in trs:
                tier.SetMedia( media )

        return trs

    # ------------------------------------------------------------------
    # Writer methods
    # ------------------------------------------------------------------

    def write_list(self, filename, ipustrs, ipusaudio):
        """
        Write the list of tracks: from_time to_time (in seconds).
        Last line is the audio file duration.

        @param filename (str) The list file name
        @param ipustrs (IPUsTrs)
        @param ipusaudio (IPUsAudio)

        """
        # Convert the tracks: from frames to times
        trackstimes = frames2times(self.tracks, ipusaudio.get_channel().get_framerate())

        with codecs.open(filename ,'w', encoding) as fp:
            idx = 0

            for (from_time,to_time) in trackstimes:
                fp.write( "%.4f %.4f " %(from_time,to_time))

                # if we assigned a filename to this tracks...
                if len(ipustrs.get_names()) > 0 and idx < len(ipustrs.get_names()):
                    ustr = ipustrs.get_names()[idx].encode('utf8')
                    fp.write( ustr.decode(encoding)+"\n" )
                else:
                    fp.write( "\n" )

                idx = idx+1

            # Finally, print audio duration
            fp.write( "%.4f\n" %ipusaudio.get_channel().get_duration() )

    # ------------------------------------------------------------------

    def write_tracks(self, ipustrs, ipusaudio, output, extensiontrs, extensionaudio):
        """
        Write tracks in an output directory.

        Print only errors in a log file.

        @param output      Directory name (String)
        @param ext         Tracks file names extension (String)

        """
        if not os.path.exists( output ):
            os.mkdir( output )

        if extensiontrs is not None:
            self.write_text_tracks(ipustrs, ipusaudio, output, extensiontrs)

        if extensionaudio is not None:
            self.write_audio_tracks(ipustrs, ipusaudio, output, extensionaudio)

    # ------------------------------------------------------------------

    def write_text_tracks(self, ipustrs, ipusaudio, output, extension):
        """
        Write the units in track files.

        """
        if not os.path.exists( output ):
            os.mkdir( output )

        if extension is None:
            raise IOError('An extension is required to write units.')

        # Get units and names
        units = ipustrs.get_units()
        names = ipustrs.get_names()

        # Convert the tracks: from frames to times
        trackstimes = frames2times(self.tracks, ipusaudio.get_channel().get_framerate())

        # Write text tracks
        for i,track in enumerate(trackstimes):
            trackbasename = ""
            if len(names) > 0 and len(names[i])>0:
                # Specific names are given
                trackbasename = os.path.join(output, names[i])
            else:
                trackbasename = os.path.join(output, "track_%.06d" % (i+1))

            tracktxtname = trackbasename+"."+extension
            if extension.lower() == "txt":
                self.__write_txttrack(tracktxtname, units[i])
            else:
                d = track[1] - track[0]
                self.__write_trstrack(tracktxtname, units[i], d)

    # ------------------------------------------------------------------

    def write_audio_tracks(self, ipustrs, ipusaudio, output, extension):
        """
        Write the audio in track files.

        """
        if not os.path.exists( output ):
            os.mkdir( output )

        if extension is None:
            raise IOError('An extension is required to write audio tracks.')

        if ipusaudio.get_channel() is None:
            return

        try:
            split_tracks = ipusaudio.chansil.track_data( self.tracks )
        except Exception as e:
            raise Exception('Split into tracks failed: audio corrupted: %s'%e)

        names = ipustrs.get_names()

        # Write audio tracks
        for i, split_track in enumerate(split_tracks):
            trackbasename = ""
            if len(names) > 0 and len(names[i])>0:
                # Specific names are given
                trackbasename = os.path.join(output, names[i])
            else:
                trackbasename = os.path.join(output, "track_%.06d" % (i+1))

            trackwavname = trackbasename+"."+extension
            audio_out = AudioPCM()
            audio_out.append_channel(ipusaudio.get_channel())
            try:
                audiodata.aio.save_fragment(trackwavname, audio_out, split_track)
            except Exception as e:
                raise Exception("Can't write track: %s. Error is %s"%(trackwavname,e))

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def __write_txttrack(self, trackfilename, trackcontent):
        with codecs.open(trackfilename,"w", encoding) as fp:
            fp.write(trackcontent)

    # ------------------------------------------------------------------

    def __write_trstrack(self, trackfilename, trackcontent, duration):
        begin = TimePoint( 0. )
        end   = TimePoint( duration )
        ann   = Annotation(TimeInterval(begin,end), Label(trackcontent))
        trs = Transcription()
        tier = trs.NewTier("Transcription")
        tier.Append(ann)
        annotationdata.aio.write(trackfilename, trs)

    # ------------------------------------------------------------------

