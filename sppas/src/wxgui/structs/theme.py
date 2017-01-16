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

    src.wxgui.structs.theme.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Management of a default theme, related to the look and feel of SPPAS.

"""
import wx

from wxgui.structs.wxoption import sppasWxOption
from wxgui.sp_consts import MAIN_FONTSIZE, TB_FONTSIZE, HEADER_FONTSIZE
from wxgui.sp_consts import BUTTON_ICONSIZE, MENU_ICONSIZE, TB_ICONSIZE

# ----------------------------------------------------------------------------


class sppasTheme(object):
    """
    :author:       Brigitte Bigi
    :organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    :contact:      brigitte.bigi@gmail.com
    :license:      GPL, v3
    :copyright:    Copyright (C) 2011-2016  Brigitte Bigi
    :summary:      Base class for a theme.

    The minimum required information, with a "classic" look.

    """
    COLOR1_BG = (250, 250, 245)
    COLOR1_FG = (28, 22, 22)
    COLOR2_BG = (80, 80, 100)
    COLOR2_FG = (240, 240, 230)
    FONT = (MAIN_FONTSIZE,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            False,
            '',
            wx.FONTENCODING_SYSTEM
            )

    # -----------------------------------------------------------------------

    def __init__(self):
        """ A Theme is a dictionary.

            - the key is a string identifying the use;
            - value is a wxOption().

        """
        self._choice = {}
        self.set_default()

    # -----------------------------------------------------------------------

    def get_choice(self, key):
        """ Return a value from its key. """

        return self._choice.get(key, None)

    # -----------------------------------------------------------------------

    def get_choices(self):
        """ Return the dictionary with all pairs key/value. """

        return self._choice

    # -----------------------------------------------------------------------

    def get_keys(self):
        """ Return the list of keys. """

        return self._choice.keys()

    # -----------------------------------------------------------------------

    def set_default(self):
        """ Fix a set of default settings for a Graphical User Interface. """

        self._choice['M_BG_COLOUR'] = sppasWxOption('wx.Colour', sppasTheme.COLOR1_BG, "Main background color")
        self._choice['M_FG_COLOUR'] = sppasWxOption('wx.Colour', sppasTheme.COLOR1_FG, "Main foreground color")
        self._choice['M_FONT'] = sppasWxOption('wx.Font', sppasTheme.FONT, "Font")

        self._choice['M_TIPS'] = sppasWxOption('bool', True, 'Show tips at start-up')
        self._choice['M_OUTPUT_EXT'] = sppasWxOption('str',  '.xra', "Output file format")
        self._choice['M_ICON_THEME'] = sppasWxOption('str',  'Default', "Icons theme")

        self._choice['M_BGD_COLOUR'] = sppasWxOption('wx.Colour', sppasTheme.COLOR2_FG, "Secondary main background color")
        self._choice['M_FGD_COLOUR'] = sppasWxOption('wx.Colour', sppasTheme.COLOR2_BG, "Secondary main foreground color")

        # Menu
        self._choice['M_BGM_COLOUR'] = sppasWxOption('wx.Colour', sppasTheme.COLOR2_BG, "Menu background color")
        self._choice['M_FGM_COLOUR'] = sppasWxOption('wx.Colour', sppasTheme.COLOR2_FG, "Menu foreground color")

        self._choice['F_SPACING'] = sppasWxOption('int', 2)

        self._choice['M_MENU_ICONSIZE'] = sppasWxOption('int', MENU_ICONSIZE)
        self._choice['M_TOOLBAR_ICONSIZE'] = sppasWxOption('int', TB_ICONSIZE)
        self._choice['M_BUTTON_ICONSIZE'] = sppasWxOption('int', BUTTON_ICONSIZE)

        self._choice['M_MAIN_FONTSIZE'] = sppasWxOption('int', MAIN_FONTSIZE)
        self._choice['M_TB_FONTSIZE'] = sppasWxOption('int', TB_FONTSIZE)
        self._choice['M_HEADER_FONTSIZE'] = sppasWxOption('int', HEADER_FONTSIZE)
