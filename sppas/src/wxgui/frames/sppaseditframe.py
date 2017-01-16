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
# File: sppaseditframe.py
# ----------------------------------------------------------------------------

import wx
import logging

from baseframe                  import ComponentFrame
from wxgui.clients.sppaseditclient import SppasEditClient
from wxgui.views.settings               import SettingsDialog

from wxgui.structs.theme    import sppasTheme
from wxgui.structs.cthemes   import all_themes
from wxgui.cutils.imageutils import spBitmap
from wxgui.cutils.textutils  import TextAsNumericValidator
from wxgui.cutils.textutils  import TextAsPercentageValidator

# Demos...
from wxgui.demo.wizardDisplayDemo import WizardDisplayDemo
from wxgui.demo.PointCtrlDemo     import PointCtrlFrame
from wxgui.demo.LabelCtrlDemo     import LabelCtrlFrame
from wxgui.demo.TierCtrlDemo      import TierCtrlFrame
from wxgui.demo.TrsCtrlDemo       import TrsCtrlFrame
from wxgui.demo.WaveCtrlDemo      import WaveCtrlFrame
from wxgui.demo.DisplayCtrlDemo   import DisplayCtrlFrame

from wxgui.demo.wizardZoomDemo    import WizardZoomDemo
from wxgui.demo.wizardScrollDemo  import WizardScrollDemo
from wxgui.demo.wizardSoundDemo   import WizardSoundDemo
from wxgui.demo.wizardTrsDemo     import WizardTrsDemo

from wxgui.sp_icons import SPPASEDIT_APP_ICON


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

DEMO_DISPLAY_WIZARD_ID = wx.NewId()
DEMO_POINT_ID = wx.NewId()
DEMO_LABEL_ID = wx.NewId()
DEMO_TIER_ID = wx.NewId()
DEMO_TRS_ID = wx.NewId()
DEMO_WAVE_ID = wx.NewId()
DEMO_DISPLAY_ID = wx.NewId()
DEMO_ZOOM_WIZARD_ID = wx.NewId()
DEMO_SCROLL_WIZARD_ID = wx.NewId()
DEMO_SOUND_WIZARD_ID = wx.NewId()
DEMO_TRS_WIZARD_ID = wx.NewId()

# ----------------------------------------------------------------------------

class SppasEditFrame( ComponentFrame ):
    """
    @authors: Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL, v3
    @summary: SppasEdit allows to display annotations and sound files.

    """

    def __init__(self, parent, id, prefsIO):
        """
        Creates a new ComponentFrame instance for SppasEdit component.
        """
        arguments = {}
        arguments['files'] = []
        arguments['title'] = "SPPAS - Vizualizer"
        arguments['type']  = "ANYFILES"
        arguments['icon']  = SPPASEDIT_APP_ICON
        arguments['prefs'] = prefsIO
        ComponentFrame.__init__(self, parent, id, arguments)

        self._append_in_menu()

    # ------------------------------------------------------------------------

    def _init_members( self, args ):
        """
        Override.
        Sets the members settings.

        """
        ComponentFrame._init_members( self,args )

        if isinstance(self._prefsIO.GetTheme(), sppasTheme):
            self._prefsIO.SetTheme( all_themes.get_theme(u'Default') )

        self._fmtype = "ANYFILES"

    # ------------------------------------------------------------------------

    def _append_in_menu(self):
        """
        Append new items in a menu or a new menu in the menubar.

        """
        return
        menubar = self.GetMenuBar()
        menus = menubar.GetMenus()

        # Menu Demo
        demomainMenu = wx.Menu()
        demomainMenu.Append(DEMO_DISPLAY_WIZARD_ID, 'Main Demo', '')
        demomainMenu.Append(DEMO_POINT_ID,  'Boundaries', 'Demo of time points')
        demomainMenu.Append(DEMO_LABEL_ID,  'Labels',     'Demo of labels')
        demomainMenu.Append(DEMO_TIER_ID,   'Tiers',      'Demo of tiers')
        demomainMenu.Append(DEMO_TRS_ID,    'Transcription file', 'Demo of a whole annotated file')
        demomainMenu.Append(DEMO_WAVE_ID,   'Wave file', 'Demo of a wave file')
        demomainMenu.Append(DEMO_DISPLAY_ID, 'Display files', 'Demo of the display window')

        demozoomMenu   = wx.Menu()
        demozoomMenu.Append(DEMO_ZOOM_WIZARD_ID, 'Zooming Demo', '')

        demoscrollMenu = wx.Menu()
        demoscrollMenu.Append(DEMO_SCROLL_WIZARD_ID, 'Scrolling Demo', '')

        demowaveMenu   = wx.Menu()
        demowaveMenu.Append(DEMO_SOUND_WIZARD_ID, 'Speech sound Demo', '')

        demotrsMenu    = wx.Menu()
        demotrsMenu.Append(DEMO_TRS_WIZARD_ID, 'Ann. Files Demo', '')

        demoMenu = wx.Menu()
        demoMenu.AppendMenu(wx.ID_ANY, 'Displaying',  demomainMenu)
        demoMenu.AppendMenu(wx.ID_ANY, 'Zooming',     demozoomMenu)
        demoMenu.AppendMenu(wx.ID_ANY, 'Scrolling',   demoscrollMenu)
        demoMenu.AppendMenu(wx.ID_ANY, 'Wave Speech', demowaveMenu)
        demoMenu.AppendMenu(wx.ID_ANY, 'Ann. Files',  demotrsMenu)

        menubar.Insert(pos=1, menu=demoMenu, title='&Demo' )

        # Events
        eventslist = [ DEMO_DISPLAY_WIZARD_ID, DEMO_POINT_ID, DEMO_LABEL_ID, DEMO_TIER_ID, DEMO_TRS_ID, DEMO_WAVE_ID, DEMO_DISPLAY_ID, DEMO_ZOOM_WIZARD_ID, DEMO_SCROLL_WIZARD_ID, DEMO_SOUND_WIZARD_ID, DEMO_TRS_WIZARD_ID ]
        for event in eventslist:
            wx.EVT_MENU(self, event, self.SppasEditProcessEvent)

    # ------------------------------------------------------------------------

    def CreateClient(self, parent, prefsIO):
        """ Override. """

        return SppasEditClient(parent,prefsIO)

    # ------------------------------------------------------------------------

    def SppasEditProcessEvent(self, event):
        """
        Processes an event, searching event tables and calling zero or more
        suitable event handler function(s).  Note that the ProcessEvent
        method is called from the wxPython docview framework directly since
        wxPython does not have a virtual ProcessEvent function.
        """
        id = event.GetId()

        if id == DEMO_DISPLAY_WIZARD_ID:
            self.OnDemoDisplayWizard(event)
        elif id == DEMO_POINT_ID:
            self.OnDemoPoint(event)
        elif id == DEMO_LABEL_ID:
            self.OnDemoLabel(event)
        elif id == DEMO_TIER_ID:
            self.OnDemoTier(event)
        elif id == DEMO_TRS_ID:
            self.OnDemoTrs(event)
        elif id == DEMO_WAVE_ID:
            self.OnDemoWave(event)
        elif id == DEMO_DISPLAY_ID:
            self.OnDemoDisplay(event)
        elif id == DEMO_ZOOM_WIZARD_ID:
            self.OnDemoZoomWizard(event)
        elif id == DEMO_SCROLL_WIZARD_ID:
            self.OnDemoScrollWizard(event)
        elif id == DEMO_SOUND_WIZARD_ID:
            self.OnDemoSoundWizard(event)
        elif id == DEMO_TRS_WIZARD_ID:
            self.OnDemoTrsWizard(event)

    #-------------------------------------------------------------------------
    # Demo... Callbacks
    #-------------------------------------------------------------------------

    def OnDemoDisplayWizard(self, event):
        """
        The whole Display demo.
        """
        logging.info('Demo.')
        WizardDisplayDemo(self)

    #-------------------------------------------------------------------------

    def OnDemoPoint(self, event):
        """
        TimePoint demo.
        """
        frame = PointCtrlFrame(self, -1, 'Time Point Demo')
        frame.Show(True)

    #-------------------------------------------------------------------------

    def OnDemoLabel(self, event):
        """
        Label demo.
        """
        frame = LabelCtrlFrame(self, -1, 'Label Demo')
        frame.Show(True)

    #-------------------------------------------------------------------------

    def OnDemoTier(self, event):
        """
        Tier demo.
        """
        frame = TierCtrlFrame(self, -1, 'Tier Demo')
        frame.Show(True)

    #-------------------------------------------------------------------------

    def OnDemoTrs(self, event):
        """
        Transcription demo.
        """
        frame = TrsCtrlFrame(self, -1, 'Transcription Demo')
        frame.Show(True)

    #-------------------------------------------------------------------------

    def OnDemoWave(self, event):
        """
        Wave demo.
        """
        frame = WaveCtrlFrame(self, -1, 'Wave Demo')
        frame.Show(True)

    #-------------------------------------------------------------------------

    def OnDemoDisplay(self, event):
        """
        Display demo.
        """
        frame = DisplayCtrlFrame(self, -1, 'Display Demo')
        frame.Show(True)

    #-------------------------------------------------------------------------

    def OnDemoZoomWizard(self, event):
        """
        The whole Zoom demo.
        """
        logging.info('Demo: Zoom.')
        WizardZoomDemo(self)

    #-------------------------------------------------------------------------

    def OnDemoScrollWizard(self, event):
        """
        The whole Scroll demo.
        """
        logging.info('Demo: Scroll.')
        WizardScrollDemo(self)

    #-------------------------------------------------------------------------

    def OnDemoSoundWizard(self, event):
        """
        The whole Sound demo.
        """
        logging.info('Demo: Sound.')
        WizardSoundDemo(self)

    #-------------------------------------------------------------------------

    def OnDemoTrsWizard(self, event):
        """
        The whole Ann. files demo.
        """
        logging.info('Demo: Ann. files.')
        WizardTrsDemo(self)

    #-------------------------------------------------------------------------

    def OnSettings(self, event):
        """
        Open the Settings box.

        Override the baseframe.OnSettings to add specific panels to
        the SettingsDialog().

        """
        p = self._prefsIO.Copy()

        prefdlg = SppasEditSettingsDialog( self, p )
        res = prefdlg.ShowModal()
        if res == wx.ID_OK:
            self.SetPrefs( prefdlg.GetPreferences() )
            if self.GetParent() is not None:
                try:
                    self.GetParent().SetPrefs( self._prefsIO )
                except Exception:
                    pass
        prefdlg.Destroy()
        self._LayoutFrame()

    # ------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# class SettingsDialog, with specific settings for SppasEdit
# ----------------------------------------------------------------------------


class SppasEditSettingsDialog( SettingsDialog ):
    """
    @author:  Brigitte Bigi
    @contact: brigitte.bigi@gmail.com
    @license: GPL, v3
    @summary: This class is used to fix all user's settings, with a Dialog.

    Dialog for the user to fix all preferences.

    """
    def __init__(self, parent, prefsIO):
        """
        Create a new dialog fo fix preferences, sorted in a notebook.

        """

        SettingsDialog.__init__(self, parent, prefsIO)

        page4 = SppasEditAppearancePanel(self.notebook, self.preferences)
        self.notebook.AddPage(page4, "Appearance")

        page5 = SppasEditTimePanel(self.notebook, self.preferences)
        self.notebook.AddPage(page5, "Displayed Time")

# ----------------------------------------------------------------------------


class SppasEditAppearancePanel(wx.Panel):
    """
    Drawing area settings.

    """
    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self._prefsIO = prefsIO

        gbs = self.__create_sizer()
        self.SetSizer(gbs)

    # ------------------------------------------------------------------------

    def __create_sizer(self):

        gbs = wx.GridBagSizer(hgap=5, vgap=5)

        # ---------- Vertical zoom step , percentage

        txt_fg = wx.StaticText(self, -1, 'Vertical zoom step (percentage): ')
        gbs.Add(txt_fg, (0,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_v_zoom = wx.TextCtrl(self, size=(150, -1), validator=TextAsPercentageValidator())
        self.text_v_zoom.SetValue( str(self._prefsIO.GetValue('D_V_ZOOM')) )
        gbs.Add(self.text_v_zoom, (0,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_v_zoom.Bind(wx.EVT_TEXT, self.onVZoomChanged)

        # ---------- Tier: Label position

        txt_fg = wx.StaticText(self, -1, 'Labels position: ')
        gbs.Add(txt_fg, (1,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.labelalign = wx.Choice(self, -1, choices=['Left' , 'Centre', 'Right'])
        current = self._prefsIO.GetValue('T_LABEL_ALIGN')
        if current == wx.ALIGN_LEFT:
            self.labelalign.SetSelection(0)
        elif current == wx.ALIGN_CENTRE:
            self.labelalign.SetSelection(1)
        else:
            self.labelalign.SetSelection(2)
        gbs.Add(self.labelalign, (1,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.labelalign.Bind(wx.EVT_CHOICE, self.onLabelAlignChanged)

        # ---------- Wave: auto-scroll

        txt_fg = wx.StaticText(self, -1, 'Wave auto-scrolling: ')
        gbs.Add(txt_fg, (2,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.wavescroll = wx.CheckBox(self, -1, '', style=wx.NO_BORDER)
        self.wavescroll.SetValue(self._prefsIO.GetValue('W_AUTOSCROLL'))
        gbs.Add(self.wavescroll, (2,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.wavescroll.Bind(wx.EVT_CHECKBOX, self.onWaveScrollChanged)

        # ---------- Color scheme

        self.theme = SppasEditColourSchemePanel(self, self._prefsIO)
        gbs.Add(self.theme, (3,0), (2,2), flag=wx.EXPAND|wx.ALL, border=5)

        gbs.AddGrowableCol(1)

        return gbs

    # ------------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------------

    def onVZoomChanged(self, event):
        """
        Change the vertical zoom coefficient,
        except if the validation fails.
        """
        success = self.text_v_zoom.GetValidator().Validate(self.text_v_zoom)
        if success is False:
            return

        self.text_v_zoom.SetFocus()
        self.text_v_zoom.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text_v_zoom.Refresh()
        try:
            v = float(self.text_v_zoom.GetValue())
            self._prefsIO.SetValue('D_V_ZOOM', 'float', v)
        except Exception:
            pass

    # ------------------------------------------------------------------------

    def onLabelAlignChanged(self, event):
        """
        Change the label alignment flag,
        except if the validation fails.
        """
        choice = self.labelalign.GetCurrentSelection()
        alignchoice = [wx.ALIGN_LEFT , wx.ALIGN_CENTRE, wx.ALIGN_RIGHT]
        self._prefsIO.SetValue('T_LABEL_ALIGN', 'wx.ALIGN', alignchoice[choice])

    # ------------------------------------------------------------------------

    def onWaveScrollChanged(self, event):
        """
        Activate/Disable the Wave vertical auto-scroll.
        """
        checked = self.wavescroll.GetValue()
        self._prefsIO.SetValue('W_AUTOSCROLL', 'bool', checked)

#-----------------------------------------------------------------------------


class SppasEditColourSchemePanel(wx.Panel):
    """ Panel with a radiobox to choose the SppasEdit Theme-Colour. """

    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self.preferences = prefsIO

        themekeys = sorted(all_themes.get_themes().keys())
        currenttheme = prefsIO.GetTheme()
        choices = []
        currentchoice = 0
        for (i,choice) in enumerate(themekeys):
            choices.append( choice )
            if currenttheme == all_themes.get_theme(choice):
                currentchoice = i

        self.radiobox = wx.RadioBox(self, label="Theme Colour scheme: ",
                                    choices=choices, majorDimension=4)

        # check the current theme
        self.radiobox.SetSelection( currentchoice )

        # bind any theme change
        self.Bind(wx.EVT_RADIOBOX, self.radioClick, self.radiobox)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.radiobox, 1, wx.EXPAND|wx.ALL, border=5)
        self.SetSizer(vbox)


    def radioClick(self, event):
        """ Set the new theme. """
        theme = all_themes.get_theme( self.radiobox.GetStringSelection() )
        self.preferences.SetTheme( theme )

# ----------------------------------------------------------------------------

class SppasEditTimePanel(wx.Panel):
    """
    Time settings.
    """
    def __init__(self, parent, prefsIO):

        wx.Panel.__init__(self, parent)
        self._prefsIO = prefsIO

        gbs = self.__create_sizer()
        self.SetSizer(gbs)

    # ------------------------------------------------------------------------

    def __create_sizer(self):

        gbs = wx.GridBagSizer(hgap=5, vgap=5)

        # ---------- Duration at start-up

        txt_fg = wx.StaticText(self, -1, 'Duration (in seconds) of the displayed period at start-up: ')
        gbs.Add(txt_fg, (0,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_duration = wx.TextCtrl(self, size=(150, -1), validator=TextAsNumericValidator())
        self.text_duration.SetValue( str(self._prefsIO.GetValue('D_TIME_MAX')) )
        gbs.Add(self.text_duration, (0,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_duration.Bind(wx.EVT_TEXT, self.onTextDurationChanged)

        # ---------- Zoom step , percentage

        txt_fg = wx.StaticText(self, -1, 'Time zoom step (percentage): ')
        gbs.Add(txt_fg, (1,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_h_zoom = wx.TextCtrl(self, size=(150, -1), validator=TextAsPercentageValidator())
        self.text_h_zoom.SetValue( str(self._prefsIO.GetValue('D_H_ZOOM')) )
        gbs.Add(self.text_h_zoom, (1,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_h_zoom.Bind(wx.EVT_TEXT, self.onHZoomChanged)

        # ---------- Scroll step , percentage

        txt_fg = wx.StaticText(self, -1, 'Time scroll step (percentage): ')
        gbs.Add(txt_fg, (2,0), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_scroll = wx.TextCtrl(self, size=(150, -1), validator=TextAsPercentageValidator())
        self.text_scroll.SetValue( str(self._prefsIO.GetValue('D_SCROLL')) )
        gbs.Add(self.text_scroll, (2,1), flag=wx.ALL|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text_scroll.Bind(wx.EVT_TEXT, self.onScrollChanged)

        gbs.AddGrowableCol(1)

        return gbs


    #-------------------------------------------------------------------------
    # Callbacks
    #-------------------------------------------------------------------------

    def onTextDurationChanged(self, event):
        """
        Change the displayed duration at start-up,
        except if the validation fails.
        """
        success = self.text_duration.GetValidator().Validate(self.text_duration)
        if success is False:
            return

        self.text_duration.SetFocus()
        self.text_duration.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text_duration.Refresh()
        try:
            v = float(self.text_duration.GetValue())
            self._prefsIO.SetValue('D_TIME_MAX', 'float', v)
        except Exception:
            pass

    #-------------------------------------------------------------------------

    def onHZoomChanged(self, event):
        """
        Change the horizontal zoom coefficient,
        except if the validation fails.
        """
        success = self.text_h_zoom.GetValidator().Validate(self.text_h_zoom)
        if success is False:
            return

        self.text_h_zoom.SetFocus()
        self.text_h_zoom.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text_h_zoom.Refresh()
        try:
            v = float(self.text_h_zoom.GetValue())
            self._prefsIO.SetValue('D_H_ZOOM', 'float', v)
        except Exception:
            pass

    #-------------------------------------------------------------------------

    def onScrollChanged(self, event):
        """
        Change the scrolling coefficient,
        except if the validation fails.
        """
        success = self.text_scroll.GetValidator().Validate(self.text_scroll)
        if success is False:
            return

        self.text_scroll.SetFocus()
        self.text_scroll.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        self.text_scroll.Refresh()
        try:
            v = float(self.text_scroll.GetValue())
            self._prefsIO.SetValue('D_SCROLL', 'float', v)
        except Exception:
            pass

# ----------------------------------------------------------------------------
